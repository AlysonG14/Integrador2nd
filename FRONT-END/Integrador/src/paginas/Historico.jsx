import React from "react";
import { useNavigate } from "react-router-dom";
import { FaInstagram, FaFacebook, FaLinkedin } from "react-icons/fa";

const HistoricoDados = [
  {
    id: 1,
    tipo: "luminosidade",
    codigo: "00:1B:44:11:3A:B9",
    descricao: "OFICINA - FRESAGEM 1",
    data: "2025-08-16",
  },
  {
    id: 2,
    tipo: "luminosidade",
    codigo: "00:1B:44:11:3A:B9",
    descricao: "FMS - SISTEMA . FLEX.MAN.",
    data: "2025-03-05",
  },
  {
    id: 3,
    tipo: "temperatura",
    codigo: "00:1B:44:11:3A:BA",
    descricao: "OFICINA - FABRICAÇÃO MECÂNICA 1",
    data: "2025-12-02",
  },
  {
    id: 4,
    tipo: "temperatura",
    codigo: "00:1B:44:11:3A:B7",
    descricao: "LAB. DE ROBÓTICA 1",
    data: "2025-11-07",
  },
  {
    id: 5,
    tipo: "umidade",
    codigo: "00:1B:44:11:3A:BA",
    descricao: "CNC FERRAMENTARIA",
    data: "2025-11-13",
  },
  {
    id: 6,
    tipo: "umidade",
    codigo: "00:1B:44:11:3A:B9",
    descricao: "OFICINA - COMANDOS ELÉTRICOS ",
    data: "2025-07-25",
  },
  {
    id: 7,
    tipo: "temperatura",
    codigo: "00:1B:44:11:3A:BA",
    descricao: "LAB. DE INFORMÁTICA A02",
    data: "2025-03-12",
  },
  {
    id: 8,
    tipo: "umidade",
    codigo: "00:1B:44:11:3A:BA",
    descricao: "COORDENAÇÃO CURSO SUPERIOR",
    data: "2025-04-21",
  },
  {
    id: 9,
    tipo: "temperatura",
    codigo: "00:1B:44:11:3A:BA",
    descricao: "OPP FIC",
    data: "2025-09-12",
  },
  {
    id: 10,
    tipo: "temperatura",
    codigo: "00:1B:44:11:3A:B7",
    descricao: "BAIXA REALOCAÇÃO",
    data: "2025-10-24",
  },
  {
    id: 11,
    tipo: "temperatura",
    codigo: "00:1B:44:11:3A:B9",
    descricao: "MANUTENÇÃO PREDIAL",
    data: "2025-05-18",
  },
  {
    id: 12,
    tipo: "temperatura",
    codigo: "00:1B:44:11:3A:BA",
    descricao: "ENTREPOSTO",
    data: "2025-12-23",
  },
];

export function Historico() {
  const navigate = useNavigate();
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

      {/* Lateral */}

      <div className="flex flex-1">
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
            <button
              onClick={() => navigate("/inicial/crud/")}
              className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110"
            >
              Ambientes
            </button>

            <button
              onClick={() => navigate("/inicial/crud/")}
              className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110"
            >
              Sensores
            </button>

            <button className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
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

        {/* Conteúdo */}

        <main className="flex-1">
          <section className="p-8">
            {/* Campo de Busca */}
            <div className="mb-4">
              <label
                htmlFor="buscaId"
                className="block mb-1 text-sm font-medium text-gray-700"
              >
                Buscar por ID:
              </label>
              <input
                id="buscaId"
                type="text"
                placeholder="Pesquisar ID"
                className="px-4 py-2 border rounded-md w-1/3"
              />
            </div>

            {/* Tabela */}
            <div className="bg-white shadow-md rounded-lg overflow-hidden">
              <table className="w-full text-left border-collapse">
                <thead className="bg-gray-800 text-white">
                  <tr>
                    <th className="px-6 py-3">ID</th>
                    <th className="px-6 py-3">Histórico</th>
                    <th className="px-6 py-3">Data</th>
                  </tr>
                </thead>
                <tbody>
                  {HistoricoDados.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-100 border-b">
                      <td className="px-6 py-3">{item.id}</td>
                      <td className="px-6 py-3">
                        {item.tipo} - {item.codigo} -{" "}
                        <span className="text-semibond">{item.descricao}</span>
                      </td>
                      <td className="px-6 py-3">{item.data}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
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
