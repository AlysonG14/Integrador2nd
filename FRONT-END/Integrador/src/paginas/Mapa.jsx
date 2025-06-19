import React from "react";

export default function Mapa(){
    return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-900 flex flex-col">
            <header className="bg-purple-800 text-white flex justify-between items-center px-6 py-4">
                <h1 className="flex items-center space-x-3 font-semibold text-lg">
                    <img src="images/image 16.png"></img>
                    <span>Smart City</span>
                </h1>

                <nav className="space-x-6 text-sm">
                    <a href="#about" className="hover:underline">About</a>
                    <a href="#dashboard" className="hover:underline">Dashboard</a>
                    <a href="#export" className="hover:underline">Export</a>
                </nav>

                <button
                aria-lebel="User profile"
                className="p-2 rounded-full bg-purple-700 hover:bg-purple-600"
                >

                <img className="bg-none" src="images/User.png"></img>

                </button>
            </header>

                    <div className="flex flex-1">
            <aside className="bg-gray-900 text-gray-300 w-64 p-6 flex flex-col gap-6">
                <button className="flex items-center gap-2 text-green-400 hover:text-green-500 font-semibold">
                    <img src="images/Vector.png">
                    </img>
                    <span>Voltar</span>
                </button>

                <div className="flex flex-col items-center gap-3">
                    <div className="w-20 h-20 rounded-full bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center text-white text-xl font-semibold">
                        <img src="images/image 14 (1).png"></img>
                    </div>
                    <h2 className="font-semibold text-white">Usuário</h2>
                </div>

                <nav className="flex flex-col gap-3">
                    <button className="bg-gray-800 hover:bg-gray-700 text-green-400 py-2 rounded-lg font-semibold transition">
                        Ambientes
                    </button>

                    <button className="bg-gray-800 hover:bg-gray-700 text-green-400 py-2 rounded-lg font-semibold transition">
                        Sensores
                    </button>

                    <button className="bg-gray-800 hover:bg-gray-700 text-green-400 py-2 rounded-lg font-semibold transition">
                        Histórico
                    </button>
                </nav>

                <button
                className="mt-auto flex items-center justify-center gap-2 border border-green-500 text-green-500 py-2 rounded-lg font-semibold hover:bg-green-500 hover:text-gray-900 transition"
                aria-label="Sair"
                >
                    <img src="images/Botão Ícone - Sair.png"></img>
                </button>
            </aside>
        </div>

        
    </div>

        


    )
}