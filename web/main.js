// Elementos HTML
const $list = document.getElementById('list');
const $error = document.getElementById('error');
const $spinner = document.getElementById('spinner');

const form = document.getElementById("postForm");
const output = document.getElementById("output");

const API = 'https://jsonplaceholder.typicode.com'; // API pública de testes

function showSpinner(show) {
    $spinner.style.display = show ? 'inline' : 'none';
    $spinner.textContent = "Salvo"
}

function showError(msg) {
    $error.textContent = msg || '';
}

function renderPosts(posts) {
    $list.innerHTML = posts.map(p => `
    <div class="card">
      <strong>#${p.id} — ${p.title}</strong>
      <p>${p.body}</p>
    </div>
  `).join('');
}

async function getPosts() {
    showError('');
    try {
        const res = await fetch(`${API}/posts?_limit=5`);
        if (!res.ok) {
            throw new Error(`Erro HTTP ${res.status}`);
        }
        const data = await res.json();
        renderPosts(data);
    } catch (err) {
        showError(err.message ?? 'Falha ao buscar dados');
    }
}


async function createPost() {
    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // impede recarregar a página

        const title = document.getElementById("title").value;
        const body = document.getElementById("body").value;
        const userId = document.getElementById("userId").value;

        try {
            const response = await fetch("https://jsonplaceholder.typicode.com/posts", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({title, body, userId})
            });

            if (!response.ok) {
                output.textContent = "Erro na requisição: " + response.status;
                return;
            }

            alert(`Post criado com sucesso`)
        } catch (err) {
            output.textContent = "Erro: " + err.message;
        }
    });
}

async function login() {
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
        const response = await fetch("https://api.exemplo.com/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email, senha})
        });

        if (!response.ok) {
            throw new Error("Login falhou");
        }

        const data = await response.json();
        localStorage.setItem("token", data.token); // salva token
    } catch (e) {
        output.textContent = "Erro: " + e.message;
    }
}

async function createPostToken() {
    document.getElementById("btn").addEventListener("click", async (e) => {
        const token = document.getElementById("token").value.trim(); // Pegar o token

        if (!token) {
            output.textContent = "Realize o login novamente!";
            return;
        }

        const title = document.getElementById("title").value;
        const body = document.getElementById("body").value;
        const userId = document.getElementById("userId").value;

        try {
            const response = await fetch("https://jsonplaceholder.typicode.com/posts/1", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`, // 🔑 Aqui vai o token
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({title, body, userId})
            });

            if (!response.ok) {
                output.textContent = "Erro: " + response.status;
                return;
            }

            const data = await response.json();
            // usar a resposta da api ...
        } catch (err) {
            output.textContent = "Erro: " + err.message;
        }
    });
}
