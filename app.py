from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configurar a API do Gemini
genai.configure(api_key="AIzaSyCotLBKjhEdSyXVxfcURXBhfRAjf9_Zx8Y")
model = genai.GenerativeModel('models/gemma-3-4b-it')

# Carregar o arquivo de regimento
def carregar_arquivo():
    try:
        with open("regimento.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao carregar o arquivo: {e}"

conteudo_arquivo = carregar_arquivo()

# Histórico da conversa (global, simples)
historico_conversa = []

@app.route("/", methods=["GET", "POST"])
def index():
    resposta = ""
    pergunta = ""

    if request.method == "POST":
        pergunta = request.form["mensagem"]
        if conteudo_arquivo and pergunta:

            # Montar histórico de chat em formato de diálogo
            conversa_formatada = ""
            for item in historico_conversa:
                conversa_formatada += f"Usuário: {item['pergunta']}\nGemini: {item['resposta']}\n"

            # Novo prompt com histórico + conteúdo do arquivo
            prompt = (
                f"Você é um assistente que responde com base no conteúdo do documento a seguir.\n\n"
                f"{conteudo_arquivo}\n\n"
                f"{conversa_formatada}\n"
                f"Usuário: {pergunta}\n"
                f"Gemini:"
            )

            try:
                response = model.generate_content(prompt)
                resposta = response.text

                # Armazena a nova pergunta/resposta no histórico
                historico_conversa.append({"pergunta": pergunta, "resposta": resposta})

            except Exception as e:
                resposta = f"Erro ao gerar resposta: {e}"

    return render_template("index.html", pergunta=pergunta, resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
