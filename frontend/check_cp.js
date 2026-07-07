import { Client } from 'ssh2';

const conn = new Client();

conn.on('ready', () => {
  console.log('Sunucuya bağlanıldı! Şifre sıfırlanıyor...');
  conn.exec('clpctl user:reset:password --userName=samkomksk35 --password=Pusula2026!', (err, stream) => {
    if (err) throw err;
    stream.on('close', (code, signal) => {
      conn.end();
    }).on('data', (data) => {
      console.log('ÇIKTI:\n' + data);
    }).stderr.on('data', (data) => {
      console.log('HATA ÇIKTISI:\n' + data);
    });
  });
}).connect({
  host: '37.157.255.97',
  port: 22,
  username: 'root',
  password: 'TcqJb27y6r'
});
