import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { FaInstagram, FaFacebook, FaLinkedin } from "react-icons/fa";

const dadosAmbientes = [
  {
    sig: 20400001,
    descricao: "DIRETORIA",
    ni: "SN75422",
    responsavel: "CESAR AUGUSTO DA COSTA",
  },
  {
    sig: 20400002,
    descricao: "SEGURANÇA TRABALHO",
    ni: "SN7786",
    responsavel: "ANDERSON APARECIDO FELIX",
  },
  {
    sig: 20400003,
    descricao: "ANALISTA DE QUALIDADE DE VIDA",
    ni: "SN1068960",
    responsavel: "DOMINIQUE MISSIO DE FARIA",
  },
  {
    sig: 20400004,
    descricao: "COPA",
    ni: "SN74604",
    responsavel: "ANGELO RAFAIM NETO",
  },
];

const dadosSensores = [
  {
    sensor: "luminosidade",
    mac_address: "00:1B:44:11:3A:B9",
    unidade_medida: "lux",
    latitude: -22.655811,
    longitude: -43.175686,
    status: "ativo",
  },
  {
    sensor: "luminosidade",
    mac_address: "00:1B:44:11:3A:B9",
    unidade_medida: "lux",
    latitude: -22.965823,
    longitude: -43.142896,
    status: "ativo",
  },
  {
    sensor: "luminosidade",
    mac_address: "00:1B:44:11:3A:B9",
    unidade_medida: "lux",
    latitude: -22.235498,
    longitude: -43.122896,
    status: "ativo",
  },
  {
    sensor: "luminosidade",
    mac_address: "00:1B:44:11:3A:B9",
    unidade_medida: "lux",
    latitude: -22.926847,
    longitude: -43.112896,
    status: "inativo",
  },
];

const CRUDPage = ({ dados, tipo, onDelete }) => {
  const [tab, setTab] = useState("visualizar");
  const [editando, setEditando] = useState(null)
  const [formEdicao, setFormEdicao] = useState({})

  const iniciarEdicao = (item) => {
    setEditando(item.id)
    setFormEdicao(item)
  }

  const handleCreate = async (e) => {
    e.preventDefault();
    const form = e.target;
    const dadosForm = {};
    for (let element of form.elements) {
      if (element.name) {
        dadosForm[element.name] = element.value;
      }
    }

    const rota = tipo.toLowerCase() === "sensores" ? "sensor" : "ambiente";
    const token = localStorage.getItem('token')

    try {
      await axios.post(`http://localhost:8000/${rota}/`, dadosForm, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      alert(`${tipo} criado com sucesso!`);
      e.target.reset();
    } catch (error) {
      console.error("Erro ao criar: ", error.response?.data || error.message);
      alert("Erro ao Criar!");
    }
  };

  const handleDelete = async (id) => {
    const rota = tipo.toLowerCase() === "sensores" ? "sensor" : "ambiente";
    try {
      await axios.delete(`http://localhost:8000/${rota}/${id}`);
      alert(`${tipo} deletado com sucesso!`);
      onDelete();
    } catch (error) {
      console.error("Erro ao deletar: ", error);
      alert("Erro ao Deletar!");
    }
  };

  const salvarEdicao = async (id) => {
    const rota = tipo.toLowerCase() === 'sensores' ? "sensor" : "ambiente"
    const token = localStorage.getItem("token")

    try {
      await axios.put(`http://localhost:8000/${rota}/${id}/`, formEdicao, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "aplications/json",
        },
      });
      alert(`${tipo} Atualizado com sucesso`)
      setEditando(null);
      onDelete();
    } catch (error) {
      console.error("Erro ao atualizar", error)
      alert("Erro ao atualizar!")
    }
  };

  return (
    <div className="p-4 bg-white rounded-xl shadow-md w-full max-w-6xl mx-auto">
      <h1 className="text-3xl font-semibold text-gray-800 mb-6 text-center">
        CRUD de {tipo}
      </h1>

      <div className="flex flex-wrap justify-center gap-3 mb-6">
        {["criar", "visualizar", "atualizar", "deletar"].map((op) => (
          <button
            key={op}
            onClick={() => setTab(op)}
            className={`px-6 py-2 rounded-full font-medium transition-all duration-200
                         ${
                           tab === op
                             ? "bg-green-600 text-white shadow"
                             : "bg-gray-100 text-gray-700 hover:bg-green-100"
                         }`}
          >
            {op.charAt(0).toUpperCase() + op.slice(1)}
          </button>
        ))}
      </div>

      {tab === "criar" && (
        <form onSubmit={handleCreate} className="space-y-4 max-w-xl mx-auto">
          {Object.keys(dados[0] || {})
          .map((campo) => (
            <input
              key={campo}
              name={campo}
              type={
                campo.toLowerCase().includes("latitude") ||
                campo.toLowerCase().includes("longitude") ||
                campo.toLowerCase().includes("valor")
                  ? "number"
                  : "text"
              }
              placeholder={campo}
              className="border border-gray-300 px-4 py-2 w-full rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
              required
            />
          ))}
          <button
            type="submit"
            className="bg-green-600 text-white px-6 py-2 rounded-md w-full hover:bg-green-700 transition-all"
          >
            Criar
          </button>
        </form>
      )}

      {(tab === "visualizar" || tab === "atualizar" || tab === "deletar") && (
        <div className="overflow-auto">
          <table className="min-w-full table-auto border border-gray-200">
            <thead className="bg-gray-100">
              <tr>
                {Object.keys(dados[0] || {}).map((chave) => (
                  <th
                    key={chave}
                    className="px-4 py-2 text-left text-gray-600 font-medium border-b"
                  >
                    {chave}
                  </th>
                ))}
                {tab !== "visualizar" && (
                  <th className="px-4 py-2 border-b">Ação</th>
                )}
              </tr>
            </thead>
            <tbody>
              {dados.map((item, index) => (
                <tr key={index} className="even:bg-gray-50">
                  {Object.keys(dados[0]).map((campo) => (
                    <td
                      key={campo}
                      className="px-4 py-2 border-b text-sm text-gray-700">
                        {editando === item.id ? (
                          <input
                          value={formEdicao[campo] || ""}
                          onChange={(e) => 
                            setFormEdicao((prev) => ({...prev, [campo]: e.target.value }))
                          } className="border border-gray-300 px-2 py-1 rounded w-full" 
                          />
                        ) : campo === 'status' ? (
                          item[campo] === true || item[campo] === 'True' ? "ativo" : "inativo"
                          ) : (
                            item[campo]
                        )}
                    </td>
                  ))}
                  {tab === "atualizar" && (
                    <td className="px-4 py-2 border-b">
                      {editando === item.id ? (
                        <button onClick={() => salvarEdicao(item.id)} className="text-green-600 hover:underline">
                          Salvar
                        </button> 
                      ) : (
                         <button onClick={() => iniciarEdicao(item)} className="hover:underline">Editar</button>
                      )}
                    </td>
                  )}
                  {tab === "deletar" && (
                    <td className="px-4 py-2 border-b">
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="hover:underline"
                      >
                        Deletar
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export function CRUD() {
  const [entidade, setEntidade] = useState("sensores");
  const [dados, setDados] = useState([]);
  const navigate = useNavigate();

  const fetchDados = () => {
    const rota = entidade === "sensores" ? "sensor" : "ambiente";
    const token = localStorage.getItem("token");

    axios
      .get(`http://localhost:8000/${rota}/`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      })
      .then((res) => setDados(res.data.results))
      .catch((err) => console.error(`Erro ao buscar ${entidade}:`, err));
  };
  
  useEffect(() => {
    fetchDados();
  }, [entidade]);

  const handleDelete = (id) => {
    setDados((prev) => prev.filter((d) => d.id !== id));
  };

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-900 flex flex-col">
      {/* Cabeçalho */}

      <header className="bg-purple-800 text-white flex items-center justify-between px-10 py-1">
        <h1 className="flex items-center space-x-3 font-semibold text-lg">
          <img src="/images/SmartCityLogo.png" alt="Logo"></img>
          <span className="text-3xl font-semibold">Smart City</span>
        </h1>

        <div className="flex items-center gap-6">
          <nav className="absolute right-40 flex gap-20 text-xl font-semibold">
            <a href="/inicial/mapa/" className="hover:underline">
              Mapa
            </a>
            <a href="/inicial/grafico/" className="hover:underline">
              Gráficos
            </a>
            <a href="/inicial/exportacao/" className="hover:underline">
              Exportar
            </a>
          </nav>
        </div>

        <button>
          <img
            src="/images/UsuárioLogo.png"
            alt="Usuário"
            className="bg-none"
          ></img>
        </button>
      </header>

      <div className="flex flex-1">
        {/* Lateral */}

        <aside className="bg-gray-900 text-gray-300 w-64 p-6 flex flex-col gap-6">
          <button
            onClick={() => navigate("/inicial/")}
            className="flex items-center gap-2 text-green-400 text-white transition-transform duration-1000 hover:scale-110"
          >
            <img src="/images/Voltar.png" alt="Voltar"></img>
            <span>Voltar</span>
          </button>

          <div className="flex flex-col items-center gap-3">
            <div className="w-24 h-24 rounded-full bg-gray-800 shadow-lg overflow-hidden">
              <img
                src="/images/Usuário.png"
                alt="Avatar do Usuário"
                className="object-cover w-full h-full"
              ></img>
            </div>
            <h2 className="text-white text-xl font-bold">Usuário</h2>
          </div>

          <nav className="flex flex-col gap-3">
            <button className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
              Ambientes
            </button>

            <button className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
              Sensores
            </button>

            <button
              onClick={() => navigate("/inicial/historico/")}
              className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110"
            >
              Histórico
            </button>
          </nav>

          <button
            onClick={() => navigate("/login/")}
            className="mt-auto flex items-center justify-center gap-2 border border-green-700 text-white text-xl px-4 py-2 rounded-md font-semibold transition-transform duration-1000 hover:scale-110"
          >
            <img
              src="/images/Botão Ícone - Sair.png"
              alt="Sair Ícone"
              className="p-1 bg-green-700 rounded-full w-13 h-13"
            ></img>
            <span>Sair</span>
          </button>
        </aside>

        {/* Principal */}

        <main className="flex-1 p-6 bg-gradient-to-br from-gray-100 to-gray-200">
          <div className="flex flex-col items-center mt-10">
            <div className="flex flex-col items-center">
              <div className="flex justify-center gap-6 mb-6">
                <button
                  onClick={() => setEntidade("sensores")}
                  className={`px-6 py-2 rounded-full font-semibold transition-all ${
                    entidade === "sensores"
                      ? "bg-purple-600 text-white shadow"
                      : "bg-white text-gray-700 hover:bg-purple-100"
                  }`}
                >
                  Sensores
                </button>
                <button
                  onClick={() => setEntidade("ambientes")}
                  className={`px-6 py-2 rounded-full font-semibold transition-all ${
                    entidade === "ambientes"
                      ? "bg-purple-600 text-white shadow"
                      : "bg-white text-gray-700 hover:bg-purple-100"
                  }`}
                >
                  Ambientes
                </button>
              </div>
              <CRUDPage
                dados={dados}
                tipo={entidade.charAt(0).toUpperCase() + entidade.slice(1)} 
                onDelete={fetchDados}
              />
            </div>
          </div>
        </main>
      </div>

      <footer className="bg-purple-800 text-white px-6 py-10 w-full">
        {/* Rodapé */}

        <div className="max-w-screen mx-auto flex flex-col lg:flex-row justify-between gap-10">
          <section className="flex-1">
            <h2 className="text-lg font-semibold mb-4">
              Envie o seu e-mail para mais notificações:
            </h2>
            <form className="flex items-center gap-2 mb-6">
              <input
                type="email"
                placeholder="Seu e-mail"
                className="p-2 rounded-md text-gray-800 w-full max-w-xs"
                required
              />
              <button
                type="submit"
                className="bg-green-600 px-4 py-2 rounded-md hover:bg-green-600 transition"
              >
                Enviar
              </button>
            </form>
            <div className="flex items-center gap-4 text-2xl">
              <a
                href="#"
                aria-label="Instagram"
                className="hover:text-gray-300"
              >
                <FaInstagram />
              </a>
              <a href="#" aria-label="Facebook" className="hover:text-gray-300">
                <FaFacebook />
              </a>
              <a href="#" aria-label="Linkedin" className="hover:text-gray-300">
                <FaLinkedin />
              </a>
            </div>
          </section>

          <section className="flex-1">
            <h2 className="text-lg font-semibold mb-4">Fale Conosco:</h2>
            <form className="space-y-3">
              <input
                type="text"
                placeholder="Nome"
                className="p-2 rounded-md text-gray-800 w-full"
                required
              />
              <input
                type="email"
                placeholder="Email"
                className="p-2 rounded-md text-gray-800 w-full"
                required
              />
              <input
                type="text"
                placeholder="Assunto"
                className="p-2 rounded-md text-gray-800 w-full"
                required
              />
              <textarea
                placeholder="Mensagem"
                className="p-2 rounded-md text-gray-800 w-full h-24 resize-none"
                required
              />
              <button
                type="submit"
                className="bg-green-600 px-4 py-2 rounded-md hover:bg-green-600 transition"
              >
                Enviar
              </button>
            </form>
          </section>
        </div>

        <div className="mt-10 border-t border-purple-600 pt-6 text-sm text-center">
          <div className="flex flex-col lg:flex-row items-center justify-between gap-4 max-w-screen-xl mx-auto">
            <div className="flex items-center gap-2 justify-center">
              <img
                src="/images/SmartCityLogo.png"
                alt="SmartCity Logo"
                className="w-12 h-12"
              ></img>
              <span>© Copyright2025 - Smart City </span>
            </div>
            <div className="flex items-center gap-4">
              <a href="#">Informações</a>
              <a href="#">Política de Privacidade</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
