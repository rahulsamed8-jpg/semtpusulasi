import streamlit as st
import json
import os
import requests
import subprocess
import tempfile
import zipfile
import random
import asyncio
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv
import google.generativeai as genai

try:
    from moviepy import ImageSequenceClip, AudioFileClip, CompositeAudioClip, VideoFileClip
    import yt_dlp
    import edge_tts
    import imageio_ffmpeg
except ImportError as e:
    st.error(f"Kütüphane hatası: {e}")

load_dotenv()

# Ayarlar
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "data", "turizm_data.json")

def load_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_caption(place_data, user_api_key=None):
    api_key = user_api_key
    if not api_key:
        api_key = "AQ.Ab8RN6JkFw7wJOW4qbMvUkRUGjVXKYsRKxT1qeCKNQC6pThigQ" # Kullanıcının verdiği çalışan anahtar
        
    prompt = f"""Sen profesyonel bir sosyal medya yöneticisisin. 
Şu mekan için Instagram ve TikTok'ta paylaşılacak, çok dikkat çekici, samimi ve bol emojili bir gönderi metni (caption) hazırla:
Mekan Adı: {place_data.get('name', '')}
Kategori: {place_data.get('category', 'Yerel İşletme')}
Bölge: {place_data.get('region', '')}
Adres: {place_data.get('address', '')}

Metin, insanları burayı ziyaret etmeye ikna etmeli. 
Gönderinin en sonuna Tiktok ve Instagram algoritması için mükemmel hashtagler (#) ayarla.
Ayrıca metnin sonuna kesinlikle şu sitemizin linkini ekle:
Daha fazla detay için sitemizi ziyaret edin: https://semtpusulasi.com/mekan/{place_data.get('slug', '')}"""

    try:
        genai.configure(api_key=api_key)
        # Try a standard model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Gemini API çökerse veya yetki hatası verirse çevrimdışı şablon kullan!
        name = place_data.get('name', '')
        cat = place_data.get('category', 'Mekan').lower()
        reg = place_data.get('region', 'İzmir')
        addr = place_data.get('address', '')
        slug = place_data.get('slug', '')
        reg_tag = reg.replace(' ', '').lower()
        cat_tag = cat.replace(' ', '').lower()
        
        t1 = f"✨ {reg} bölgesinde keşfedilmeyi bekleyen harika bir yer! 🤩\n\nBugün {name} adlı {cat} noktasına yakından bakıyoruz. Atmosferi ve kalitesiyle listene kesinlikle eklemen gereken bir adres. 📌 Hemen bu mekanı kaydet ve arkadaşlarına gönder! 👇\n\n📍 Adres: {addr}\n\nDaha fazla detay için sitemizi ziyaret edin: https://semtpusulasi.com/mekan/{slug}\n\n#semtpusulasi #{reg_tag} #mekanönerisi #keşfet #tiktok #instagram"
        
        t2 = f"🚨 {reg} turumuzda durak noktamız: {name}! 🌟\n\nEğer kaliteli bir {cat} arıyorsan burası tam sana göre! Hafta sonu planlarınız için harika bir alternatif olabilir. Gidenler yorumlarda buluşsun! 👇😎\n\n📍 Adres: {addr}\n\nDaha fazla detay için sitemizi ziyaret edin: https://semtpusulasi.com/mekan/{slug}\n\n#semtpusulasi #{reg_tag} #{cat_tag} #izmir #gezilecekyerler"
        
        t3 = f"🔥 {reg} sakinleri ve yolu düşenler dikkat! 📣\n\n{name}, sunduğu harika deneyimle {cat} severlerin yeni favorisi! Biz denedik, çok beğendik. Siz de mutlaka şans verin. 💯\n\n📍 Konum: {addr}\n\nDaha fazla detay için sitemizi ziyaret edin: https://semtpusulasi.com/mekan/{slug}\n\n#semtpusulasi #{reg_tag} #mekankeşfi #tiktokkeşfet"
        
        return random.choice([t1, t2, t3])


def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload"}
    try:
        with open(file_path, "rb") as f:
            files = {"fileToUpload": f}
            response = requests.post(url, data=data, files=files)
            if response.status_code == 200:
                return response.text.strip()
    except Exception as e:
        pass
    return None

def trigger_make_webhook(caption, image_urls):
    webhook_url = "https://hook.eu1.make.com/plsl7e44fvb2toeullwjo8t71n67mkxy"
    payload = {
        "caption": caption
    }
    for i, url in enumerate(image_urls):
        payload[f"image{i+1}"] = url

    try:
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except:
        return False


def download_youtube_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        return False

async def generate_voiceover_async(text, output_path):
    import re
    clean_text = re.sub(r'#\w+', '', text)
    clean_text = re.sub(r'http\S+', '', clean_text)
    clean_text = clean_text.replace('\n', ' ').strip()
    voice = "tr-TR-EmelNeural"
    communicate = edge_tts.Communicate(clean_text, voice)
    await communicate.save(output_path)

def generate_voiceover(text, output_path):
    try:
        asyncio.run(generate_voiceover_async(text, output_path))
    except Exception as e:
        pass

def create_tiktok_video(place_data, youtube_url, caption_text):
    if not place_data.get("photos") or len(place_data["photos"]) == 0:
        st.error("Bu mekanın fotoğrafı yok!")
        return None
        
    temp_dir = tempfile.mkdtemp()
    photos = place_data["photos"][:5]
    generated_files = []
    
    for i, p_url in enumerate(photos):
        try:
            url = p_url.replace("maxwidth=800", "maxwidth=1080")
            r = requests.get(url)
            img = Image.open(BytesIO(r.content)).convert("RGBA")
            
            target_w, target_h = 1080, 1920
            img_w, img_h = img.size
            
            ratio = max(target_w / img_w, target_h / img_h)
            new_size = (int(img_w * ratio), int(img_h * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            left = (new_size[0] - target_w) / 2
            top = (new_size[1] - target_h) / 2
            right = (new_size[0] + target_w) / 2
            bottom = (new_size[1] + target_h) / 2
            img = img.crop((left, top, right, bottom)).convert("RGB")
            
            img_path = os.path.join(temp_dir, f"{place_data['slug']}_video_0{i+1}.jpg")
            img.save(img_path)
            generated_files.append(img_path)
        except Exception:
            continue
            
    if not generated_files:
        st.error("Hiçbir resim hazırlanamadı.")
        return None

    video_path = os.path.join(temp_dir, f"{place_data['slug']}_tiktok.mp4")
    try:
        vo_path = os.path.join(temp_dir, "voiceover.mp3")
        generate_voiceover(caption_text, vo_path)
        
        audio_clips = []
        vo_duration = 10.0
        if os.path.exists(vo_path):
            vo_clip = AudioFileClip(vo_path)
            audio_clips.append(vo_clip)
            vo_duration = vo_clip.duration
            
        time_per_image = max(3.0, (vo_duration + 1.0) / len(generated_files))
        
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        silent_video = os.path.join(temp_dir, "silent_video.mp4")
        
        fps = 25
        frames_per_image = int(time_per_image * fps)
        
        inputs = []
        filter_complex = []
        concat_inputs = []
        
        for i, img_file in enumerate(generated_files):
            inputs.extend(['-i', img_file])
            filter_complex.append(f"[{i}:v]zoompan=z='min(zoom+0.0015,1.5)':d={frames_per_image}:s=1080x1920:fps={fps}[v{i}]")
            concat_inputs.append(f"[v{i}]")
            
        filter_string = ";".join(filter_complex) + ";"
        filter_string += "".join(concat_inputs) + f"concat=n={len(generated_files)}:v=1:a=0,format=yuv420p[outv]"
        
        cmd = [
            ffmpeg_exe, '-y',
            *inputs,
            '-filter_complex', filter_string,
            '-map', '[outv]',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-r', str(fps),
            silent_video
        ]
        
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        clip = VideoFileClip(silent_video)
        
        if youtube_url:
            bg_path = os.path.join(temp_dir, "bg_music.mp3")
            if download_youtube_audio(youtube_url, bg_path):
                if os.path.exists(bg_path):
                    bg_clip = AudioFileClip(bg_path).multiply_volume(0.1)
                    if bg_clip.duration > clip.duration:
                        bg_clip = bg_clip.subclipped(0, clip.duration)
                    audio_clips.append(bg_clip)
                    
        if audio_clips:
            final_audio = CompositeAudioClip(audio_clips).with_duration(clip.duration)
            clip = clip.with_audio(final_audio)
            
        clip.write_videofile(video_path, fps=fps, codec="libx264", audio_codec="aac", logger=None)
        
        try:
            clip.close()
            if os.path.exists(vo_path): vo_clip.close()
        except:
            pass
            
        return video_path
    except Exception as e:
        st.error(f"Video oluşturulurken hata: {str(e)}")
        return None

def create_carousel_post(place_data):
    if not place_data.get("photos") or len(place_data["photos"]) == 0:
        st.error("Bu mekanın fotoğrafı yok!")
        return None
        
    temp_dir = tempfile.mkdtemp()
    photos = place_data["photos"][:5] # En fazla 5 resim
    
    # Logonun yüklenmesi
    logo = None
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "logo.png")
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo_w = 150
            logo_h = int(logo.height * (logo_w / logo.width))
            logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    except:
        pass

    generated_files = []
    
    for i, p_url in enumerate(photos):
        try:
            url = p_url.replace("maxwidth=800", "maxwidth=1080")
            r = requests.get(url)
            img = Image.open(BytesIO(r.content)).convert("RGBA")
            
            # Resmi 1080x1350 (Dikey / Vertical) boyutuna kırp (Center Crop)
            target_w, target_h = 1080, 1350
            img_w, img_h = img.size
            
            # Hedef boyutu kaplayacak şekilde orantılı büyüt/küçült
            ratio = max(target_w / img_w, target_h / img_h)
            new_size = (int(img_w * ratio), int(img_h * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Merkeze alarak kırp
            left = (new_size[0] - target_w) / 2
            top = (new_size[1] - target_h) / 2
            right = (new_size[0] + target_w) / 2
            bottom = (new_size[1] + target_h) / 2
            img = img.crop((left, top, right, bottom))
            
            if logo:
                img.paste(logo, (1080 - logo_w - 30, 30), logo)
            
            img = img.convert("RGB")
            
            img_path = os.path.join(temp_dir, f"{place_data['slug']}_0{i+1}.jpg")
            img.save(img_path)
            generated_files.append(img_path)
        except Exception as e:
            st.warning(f"Resim {i+1} işlenirken hata: {str(e)}")
            continue
            
    if not generated_files:
        st.error("Hiçbir resim hazırlanamadı.")
        return None
        
    return generated_files


st.set_page_config(page_title="Semt Pusulası - İçerik Stüdyosu", page_icon="🧭", layout="wide")

st.sidebar.title("⚙️ Ayarlar")
user_gemini_key = st.sidebar.text_input("Gemini API Key (Opsiyonel)", type="password", help="Eğer .env dosyasında yoksa buraya yapıştırabilirsiniz.")

st.title("🧭 Semt Pusulası İçerik Stüdyosu")
st.markdown("Veritabanındaki mekanları kullanarak tek tuşla sosyal medya (Instagram/Facebook) gönderileri oluşturun.")

data = load_data()
place_names = [p["name"] for p in data]

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Mekan Seçimi")
    selected_name = st.selectbox("Bir mekan seçin:", place_names)
    selected_place = next(p for p in data if p["name"] == selected_name)
    
    st.write("**Kategori:**", selected_place.get("category", "-"))
    st.write("**Bölge:**", selected_place.get("region", "-"))
    st.write("**Adres:**", selected_place.get("address", "-"))
    
    st.markdown("---")
    st.subheader("Instagram Kaydırmalı Gönderi")
    if st.button("🎞️ Kaydırmalı (Carousel) Post Üret (Max 5 Görsel)", use_container_width=True):
        with st.spinner("Kaydırmalı post görselleri ve Yapay Zeka Metni hazırlanıyor..."):
            result_files = create_carousel_post(selected_place)
            caption = generate_caption(selected_place, user_gemini_key)
            if result_files:
                st.session_state['generated_carousel_files'] = result_files
                st.session_state['generated_caption'] = caption
                st.session_state.pop('generated_video_file', None)
                
    st.markdown("---")
    st.subheader("TikTok / Reels Video Üretimi")
    yt_link = st.text_input("Arka Plan Müziği (YouTube Linki) - Opsiyonel", placeholder="https://www.youtube.com/watch?v=...")
    if st.button("🎥 TikTok & Reels Videosu Üret (Seslendirmeli)", use_container_width=True):
        with st.spinner("Video üretiliyor (Bu işlem bilgisayar hızına göre 30-60 saniye sürebilir)..."):
            caption = generate_caption(selected_place, user_gemini_key)
            st.session_state['generated_caption'] = caption
            video_file = create_tiktok_video(selected_place, yt_link, caption)
            if video_file:
                st.session_state['generated_video_file'] = video_file
                st.session_state.pop('generated_carousel_files', None)

with col2:
    st.subheader("Üretilen İçerik Önizlemesi")
    if 'generated_carousel_files' in st.session_state or 'generated_video_file' in st.session_state:
        st.success("İçerik başarıyla hazırlandı!")
        
        st.subheader("📝 Yapay Zeka Gönderi Metni")
        st.text_area("Bu metni kopyalayıp paylaşabilirsiniz:", 
                     st.session_state.get('generated_caption', ''), 
                     height=200)
                     
        if 'generated_carousel_files' in st.session_state:
            st.subheader("🖼️ Hazırlanan Görseller")
            st.markdown("*Görsellere sağ tıklayıp 'Resmi Farklı Kaydet' diyerek indirebilirsiniz.*")
            files = st.session_state['generated_carousel_files']
            cols = st.columns(min(3, len(files)))
            for i, f_path in enumerate(files):
                with cols[i % len(cols)]:
                    st.image(f_path, caption=f"Görsel {i+1}", use_container_width=True)
            st.markdown("---")
            st.subheader("🤖 Otomasyon")
            st.info("Aşağıdaki butona bastığınızda görselleriniz Make.com'a iletilir.")

        if 'generated_video_file' in st.session_state:
            st.subheader("🎥 Üretilen Video")
            video_file = st.session_state['generated_video_file']
            st.video(video_file)
            with open(video_file, "rb") as f:
                st.download_button("📥 Videoyu İndir (MP4)", data=f, file_name="tiktok_reels.mp4", mime="video/mp4", use_container_width=True)
        
        if st.button("🚀 Sosyal Medyada Otomatik Paylaş (Make.com)", use_container_width=True):
            with st.spinner("Görseller sunucuya (Catbox) yükleniyor... Bu biraz sürebilir."):
                public_urls = []
                for f_path in files:
                    p_url = upload_to_catbox(f_path)
                    if p_url:
                        public_urls.append(p_url)
                
            if public_urls:
                with st.spinner("Make.com'a veri gönderiliyor..."):
                    caption = st.session_state.get('generated_caption', '')
                    success = trigger_make_webhook(caption, public_urls)
                    if success:
                        st.success("Tebrikler! Make.com senaryosu tetiklendi. Veriler Make.com'a başarıyla ulaştı!")
                    else:
                        st.error("Make.com'a veri gönderilirken hata oluştu.")
            else:
                st.error("Görseller yüklenemediği için iptal edildi.")
                
    else:
        st.info("Henüz bir içerik üretilmedi. Soldaki butonlara basarak üretebilirsiniz.")
