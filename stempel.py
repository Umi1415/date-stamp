import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

st.title("Tambah Tanggal di Atas Gambar dan Simpan")

# Upload gambar
uploaded_image = st.file_uploader("Unggah gambar", type=["png", "jpg", "jpeg"])

# Pilih tanggal dari kalender
selected_date = st.date_input("Pilih Tanggal", value=datetime.date.today())
formatted_date = selected_date.strftime("%d-%m-%Y")  # Format tanggal: 08-07-2025

# Ukuran dan warna teks
font_size = st.slider("Ukuran Teks", min_value=10, max_value=100, value=30)
text_color = st.color_picker("Pilih Warna Teks", "#000000")

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGBA")
    image_width, image_height = image.size

    # Gambar awal (dengan tanggal di tengah)
    initial_drawing = {
        "objects": [
            {
                "type": "text",
                "left": image_width // 2,
                "top": image_height // 2,
                "text": formatted_date,
                "font": "Arial",
                "fontSize": font_size,
                "fill": text_color,
                "angle": 0,
            }
        ],
        "background": "",
    }

    st.write("Geser tanggal ke posisi yang diinginkan:")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        background_image=image,
        update_streamlit=True,
        height=image_height,
        width=image_width,
        drawing_mode="transform",
        initial_drawing=initial_drawing,
        key="canvas"
    )

    if canvas_result.json_data is not None:
        objects = canvas_result.json_data.get("objects", [])
        if len(objects) > 0 and objects[0]["type"] == "text":
            text_x = int(objects[0]["left"])
            text_y = int(objects[0]["top"])

            # Buat gambar baru dengan teks
            new_img = image.copy()
            draw = ImageDraw.Draw(new_img)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            draw.text((text_x, text_y), formatted_date, font=font, fill=text_color)

            # Tampilkan hasil
            st.image(new_img, caption="Hasil Gambar", use_column_width=True)

            # Unduh PNG
            buffer = io.BytesIO()
            new_img.save(buffer, format="PNG")
            st.download_button(
                label="Unduh Gambar",
                data=buffer.getvalue(),
                file_name="Gambar dengan tanggal.png",
                mime="image/png"
            )