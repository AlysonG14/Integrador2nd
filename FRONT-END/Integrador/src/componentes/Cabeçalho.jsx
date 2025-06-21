import React from "react";

export function Cabeçalho() {
  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-900 flex flex-col">
      {/* Cabeçalho */}

      <header className="bg-purple-800 text-white flex items-center justify-between px-10 py-1">
        <h1 className="flex items-center space-x-3 font-semibold text-lg">
          <img src="images/SmartCityLogo.png" alt="Logo"></img>
          <span className="text-3xl font-semibold">Smart City</span>
        </h1>

        <div className="flex items-center gap-6">
          <nav className="absolute right-40 flex gap-20 text-xl font-semibold">
            <a href="#Início" className="hover:underline">
              Mapa
            </a>
            <a href="#Gráfico" className="hover:underline">
              Gráficos
            </a>
            <a href="#Exportar" className="hover:underline">
              Exportar
            </a>
          </nav>
        </div>

        <button>
          <img
            src="images/UsuárioLogo.png"
            alt="Usuário"
            className="bg-none"
          ></img>
        </button>
      </header>
    </div>
  );
}
