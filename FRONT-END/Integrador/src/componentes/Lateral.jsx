import React from "react";

export function Lateral() {
  return (
    <div className="flex flex-1">
      {/* Lateral */}

      <aside className="bg-gray-900 text-gray-300 w-64 p-6 flex flex-col gap-6">
        <button className="flex items-center gap-2 text-green-400 text-white transition-transform duration-1000 hover:scale-110">
          <img src="images/Voltar.png" alt="Voltar"></img>
          <span>Voltar</span>
        </button>

        <div className="flex flex-col items-center gap-3">
          <div className="w-24 h-24 rounded-full bg-gray-800 shadow-lg overflow-hidden">
            <img
              src="images/Usuário.png"
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

          <button className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
            Histórico
          </button>
        </nav>

        <button className="mt-auto flex items-center justify-center gap-2 border border-green-700 text-white text-xl px-4 py-2 rounded-md font-semibold transition-transform duration-1000 hover:scale-110">
          <img
            src="images/Botão Ícone - Sair.png"
            alt="Sair Ícone"
            className=" p-1 bg-green-700 rounded-full w-13 h-13"
          ></img>
          <span>Sair</span>
        </button>
      </aside>
    </div>
  );
}
