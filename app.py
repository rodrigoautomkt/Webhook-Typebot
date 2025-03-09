from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = "SUA_CHAVE_OPENAI_AQUI"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API rodando corretamente!"})

@app.route("/gerar_topicos", methods=["POST"])
def gerar_topicos():
    dados = request.json
    tema = dados.get("tema")
    publico_alvo = dados.get("publico_alvo")
    problema = dados.get("problema")
    paginas = dados.get("paginas")

    if not tema or not publico_alvo or not problema or not paginas:
        return jsonify({"erro": "Faltam informações"}), 400

    prompt = f"""
    Crie uma estrutura de tópicos para um e-book sobre '{tema}'.
    Público-alvo: {publico_alvo}.
    Problema principal que será resolvido: {problema}.
    O e-book terá aproximadamente {paginas} páginas.
    Gere uma lista de tópicos bem estruturados para o conteúdo.
    """

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Você é um especialista em criação de e-books."},
                  {"role": "user", "content": prompt}]
    )

    return jsonify({"topicos": resposta["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
