🌐 CampusConnect  
> A smart and secure platform for students to access class notes, video lectures, and discussion groups.
🚀 Features  
✅ Daily Notes – Upload and access class notes conveniently  
✅ Video Lectures – Stream and download video lectures  
✅ Discussion Groups – Engage in class discussions and Q&A  
✅ User Profiles – Enhanced and secure user profiles for smarter engagement  
✅ AI-Enhanced Chatbot – Integrated with OpenAI API for smart responses  
 

🛠️ Tech Stack
| Layer           | Technology         |
|-----------------|--------------------|
| Frontend    | HTML, CSS, JavaScript |
| Backend     | Flask (Python)      |
| Database     | SQLite (for now)    |
| APIs         | None          |
| Storage       | Local (switching to S3 for scaling) |
🎯 Installation  
🔽 Clone the Repo  
bash
git clone https://github.com/your-username/CampusConnect.git
cd CampusConnect
🏗️ Set Up Environment  
1. Create a virtual environment and activate it  
bash
python -m venv venv
source venv/bin/activate
2. Install dependencies
bash
pip install -r requirements.txt
🚀 Run the App  
bash
flask run

> Open in browser → `http://127.0.0.1:5000`
 📂 Project Structure
CampusConnect/
├── app.py
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── profile.html
├── static/
│   ├── styles.css
│   ├── script.js
├── models/
│   ├── user.py
│   ├── notes.py
├── chatbot/
│   ├── chatbot.py
├── README.md
├── .gitignore
├── requirements.txt
>  🧪 Usage  
- Home Page: View announcements and latest notes  
- Login/Register: Create and manage a secure user profile  
- Discussion Groups: Start or join discussions  
- Upload Notes: Upload and organize class notes  
- Chatbot: Use the AI chatbot for quick answers  
 💡 AI Integration  
CampusConnect uses OpenAI API to enhance the chatbot for:  
✅ Answering student queries  
✅ Providing resource suggestions  
✅ Smart and contextual responses  
 🤝 Contributing  
1. Fork the repository  
2. Create a new branch (`git checkout -b feature-branch`)  
3. Commit changes (`git commit -m 'Add new feature'`)  
4. Push to the branch (`git push origin feature-branch`)  
5. Create a Pull Request  
 📄 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.  
 🌟 Acknowledgements 
- Built with ❤️ using Flask and OpenAI API  
- Inspired by the need for smarter campus engagement  
 ✅ Git Workflow* 
bash
# Stage changes
git add .

# Commit changes
git commit -m "Add new feature"

# Push to GitHub
git push origin main
