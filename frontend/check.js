import { Client } from 'ssh2';
import dotenv from 'dotenv';
dotenv.config();

const conn = new Client();
conn.on('ready', () => {
  console.log('Client :: ready');
  conn.exec('cd /home/samkomksk35/htdocs/semtpusulasi.com && chmod -R 777 mekan', (err, stream) => {
    if (err) throw err;
    stream.on('close', (code, signal) => {
      conn.end();
    }).on('data', (data) => {
      console.log('STDOUT: ' + data);
    }).stderr.on('data', (data) => {
      console.log('STDERR: ' + data);
    });
  });
}).connect({
  host: process.env.FTP_HOST,
  port: 22,
  username: process.env.FTP_USERNAME,
  password: process.env.FTP_PASSWORD
});
