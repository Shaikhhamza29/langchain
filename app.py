import streamlit as st
import cohere

# Initialize Cohere client with API key
CO_API_KEY = "z7hSXvjtmmwmXxQbUzjYU0w9NTPY1PukWFjo1LmC"
co = cohere.Client(CO_API_KEY)

def cohere_generate_doc(code, language):
    prompt = (
        f"Analyze this {language} code and create clear documentation including:\n"
        "- Class and attribute descriptions\n"
        "- Function descriptions with parameters & return values\n"
        "- Usage examples if relevant\n\n"
        f"Code:\n{code}\n\nDocumentation:\n"
    )
    try:
        response = co.chat(
            message=prompt,
            model="command-xlarge-nightly",
            max_tokens=512,
            temperature=0.3,
        )
        if hasattr(response, "generations"):
            return response.generations[0].text.strip()
        elif hasattr(response, "choices"):
            return response.choices[0].message.content.strip()
        elif hasattr(response, "text"):
            return response.text.strip()
        else:
            return str(response)
    except Exception as e:
        return f"Documentation error: {str(e)}"

st.title("Code Documentation Generater")

languages = [
    "Python", "JavaScript", "Java", "C++", "Ruby", "Go", "C#", "Swift", "Kotlin", "PHP",
    "TypeScript", "Rust", "Scala", "Haskell", "Perl", "Lua", "Shell", "R", "MATLAB", "HTML",
    "CSS", "SQL", "Dart", "Objective-C"
]

file_types = {
    "Python": "py", "JavaScript": "js", "Java": "java", "C++": "cpp", "Ruby": "rb",
    "Go": "go", "C#": "cs", "Swift": "swift", "Kotlin": "kt", "PHP": "php", "TypeScript": "ts",
    "Rust": "rs", "Scala": "scala", "Haskell": "hs", "Perl": "pl", "Lua": "lua", "Shell": "sh",
    "R": "r", "MATLAB": "m", "HTML": "html", "CSS": "css", "SQL": "sql", "Dart": "dart", "Objective-C": "m"
}

language = st.selectbox("Choose a programming language", languages)
ext = file_types[language]

uploaded = st.file_uploader(f"Upload your {language} file", type=ext)

if uploaded:
    code = uploaded.read().decode("utf-8")
    st.subheader("Generated Documentation")
    st.write(cohere_generate_doc(code, language))
