import Client from 'ssh2-sftp-client';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const config = {
    host: process.env.FTP_HOST,
    username: process.env.FTP_USERNAME,
    password: process.env.FTP_PASSWORD,
    port: 22,
    readyTimeout: 20000
};

const sftp = new Client();
const localPath = path.join(__dirname, 'dist');
const remotePath = '/home/samkomksk35/htdocs/semtpusulasi.com';

async function uploadSequential(srcDir, destDir, basePath = '') {
    const items = fs.readdirSync(srcDir);
    for (const item of items) {
        const srcPath = path.join(srcDir, item);
        const destPath = destDir + '/' + item;
        const stat = fs.statSync(srcPath);
        
        if (stat.isDirectory()) {
            const exists = await sftp.exists(destPath);
            if (!exists) {
                await sftp.mkdir(destPath, true);
            }
            await uploadSequential(srcPath, destPath, basePath + item + '/');
        } else {
            // Tam yolu göster ki dondu sanılmasın
            const displayPath = basePath + item;
            process.stdout.write(`\rYükleniyor: ${displayPath.substring(0, 60).padEnd(60)}`);
            await sftp.put(srcPath, destPath);
        }
    }
}

async function deploy() {
    try {
        console.log(`🔌 Sunucuya bağlanılıyor (${config.host})...`);
        await sftp.connect(config);
        
        console.log(`🚀 Dosyalar güvenli modda, tek tek yükleniyor...`);
        console.log(`💡 (Not: Yüklenen klasör isimleri ekranda akacaktır)`);
        
        const rootExists = await sftp.exists(remotePath);
        if (!rootExists) {
            await sftp.mkdir(remotePath, true);
        }
        
        await uploadSequential(localPath, remotePath, '');
        
        console.log('\n✅ Yükleme başarıyla tamamlandı! Site güncellendi.');
    } catch (err) {
        console.error('\n❌ Yükleme sırasında bir hata oluştu:', err.message);
    } finally {
        await sftp.end();
    }
}

deploy();
