import base64

# we need base64 since streamlit cant fetch local files for images

def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

user_img_base64 = get_image_base64("assets/kalpesh.jpg")
bot_img_base64 = get_image_base64("assets/Varys.jpg")

css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 78px;
    height: 78px;
}
.chat-message .avatar img {
    width: 78px;
    height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    padding: 0 1.5rem;
    color: #fff;
    flex: 1;
}
</style>
'''


user_template = f'''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/jpg;base64,{user_img_base64}">
    </div>    
    <div class="message">{{{{MSG}}}}</div>
</div>
'''

bot_template = f'''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/jpg;base64,{bot_img_base64}">
    </div>
    <div class="message">{{{{MSG}}}}</div>
</div>
'''

info_template = f'''
    <div style='position: fixed; bottom: 10px; left: 10px; font-size: 13px; color: gray;'>
        <b>Gyaantra</b> = Gyaan (Knowledge) + Yantra (Machine)<br>
         Made by Kalpesh
    </div>
'''