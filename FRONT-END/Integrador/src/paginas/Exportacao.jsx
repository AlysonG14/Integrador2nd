import React from "react";
import { useNavigate } from "react-router-dom";
import {FaInstagram, FaFacebook, FaLinkedin, } from "react-icons/fa";
export function Exportacao() {
  const navigate = useNavigate()
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
            <a href="#" className="hover:underline">
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
          <button onClick={()=> navigate("/inicial/")} className="flex items-center gap-2 text-green-400 text-white transition-transform duration-1000 hover:scale-110">
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
            <button onClick={()=> navigate("/inicial/crud/")} className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
              Ambientes
            </button>

            <button onClick={()=> navigate("/inicial/crud/")} className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
              Sensores
            </button>

            <button onClick={()=> navigate("/inicial/historico/")} className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
              Histórico
            </button>
          </nav>

          <button onClick={()=> navigate("/login/")} className="mt-auto flex items-center justify-center gap-2 border border-green-700 text-white text-xl px-4 py-2 rounded-md font-semibold transition-transform duration-1000 hover:scale-110">
            <img
              src="/images/Botão Ícone - Sair.png"
              alt="Sair Ícone"
              className=" p-1 bg-green-700 rounded-full w-13 h-13"
            ></img>
            <span>Sair</span>
          </button>
        </aside>

        {/* Conteúdo Principal */}

        <main className="flex-1">
          {/* Seção de Exportação */}

          <section className="p-8">
            <div className="bg-gray-900 shadow-lg rounded-xl p-5 space-y-6">
              <div className="flex justify-center items-center bg-green-700 rounded-xl px-6 py-6 space-x-4">
                <img
                  src="/images/Excel.png"
                  alt="Excel"
                  className="w-12 h-12"
                ></img>
                <h2 className="text-2xl font-bold text-white">
                  Exportação de Dados
                </h2>
              </div>

              <p className="text-[#FFFFFF] bg-gray-800 p-4 rounded-md text-justify border border-gray-700">
                Esta funcionalidade permite ao usuário exportar as informações
                exibidas na tela para um arquivo Excel (.xlsx ou .csv) de forma
                rápida e prática. Ao clicar no botão "Exportar Dados", um
                arquivo será gerado contendo todos os dados atuais, organizados
                em colunas e formatado para facilitar análises, compartilhamento
                e armazenamento externo. Os dados são: Sensores, Ambientes e
                Históricos.
              </p>

              {/* Botões de Exportação */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
                <div className="border border-green-700 p-6 bg-gray-800 rounded-xl shadow-md hover:shadow-lg transition">
                  <img
                    src="/images/Lâmpada.png" alt="Ícone de Sensores"
                    className="text-green-600 text-4xl mx-auto mb-2"
                  ></img>
                  <p className="text-lg text-white font-semibold mb-2">
                    Sensores
                  </p>
                  <button className="bg-green-600 hover:bg-green-700 hover:scale-105 transition-transform duration-300 text-white px-4 py-2 rounded font-semibold">
                    Exportar
                  </button>
                </div>
                <div className="border border-green-700 p-6 bg-gray-800 rounded-xl shadow-md hover:shadow-lg transition">
                  <img
                    src="/images/Folha.png" alt="Ícone de Ambiente"
                    className="text-green-600 bg-gray-800 rounded-xl text-4xl mx-auto mb-8"
                  ></img>
                  <p className="text-lg text-white font-semibold mb-2">
                    Ambientes
                  </p>
                  <button className="bg-green-600 hover:bg-green-700 hover:scale-105 transition-transform duration-300 text-white px-4 py-2 rounded font-semibold">
                    Exportar
                  </button>
                </div>
                <div className="border border-green-700 p-6 bg-gray-800 rounded-xl shadow-md hover:shadow-lg transition">
                  <img
                    src="/images/Histórico.png" alt="Ícone de Histórico"
                    className="text-green-600 text-4xl mx-auto mb-7"
                  ></img>
                  <p className="text-lg text-white font-semibold mb-2">
                    Histórico
                  </p>
                  <button className="bg-green-600 hover:bg-green-700 hover:scale-105 transition-transform duration-300 text-white px-4 py-2 rounded font-semibold">
                    Exportar
                  </button>
                </div>
                <div className="flex items-center gap-2 mt-6 text-white">
                  <img
                    src="/images/Ícone de Formato Excel.png"
                    alt="Ícone do Arquivo"
                    className="w-8 h-10"
                  ></img>
                  <p>Formato .xlsx ou .csv</p>
                </div>
              </div>
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
