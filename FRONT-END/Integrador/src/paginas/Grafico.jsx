import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import {FaInstagram, FaFacebook, FaLinkedin,} from "react-icons/fa"

const dadosSensores = {
    temperatura: [
        {dia: "Seg", valor: 22},
        {dia: "Ter", valor: 24},
        {dia: "Qua", valor: 23},
        {dia: "Qui", valor: 25},
        {dia: "Sex", valor: 21},
    ],
    umidade: [
        {dia: "Seg", valor: 70},
        {dia: "Ter", valor: 65},
        {dia: "Qua", valor: 75},
        {dia: "Qui", valor: 68},
        {dia: "Sex", valor: 60},
    ],
    luminosidade: [
        {dia: "Seg", valor: 400},
        {dia: "Ter", valor: 420},
        {dia: "Qua", valor: 390},
        {dia: "Qui", valor: 450},
        {dia: "Sex", valor: 470},
    ],
    contador: [
        {dia: "Seg", valor: 120},
        {dia: "Ter", valor: 90},
        {dia: "Qua", valor: 110},
        {dia: "Qui", valor: 100},
        {dia: "Sex", valor: 130}, 
    ],
};

export function Grafico(){
    const navigate = useNavigate()

    const [sensorSelecionado, setSensorSelecionado] = useState(null)

    const sensores = [
        { tipo: "temperatura", label: "Temperatura", img: "/images/Temperatura.png" },
        { tipo: "luminosidade", label: "Luminosidade", img: "/images/Luminosidade.png" },
        { tipo: "umidade", label: "Umidade", img: "/images/Umidade.png" },
        { tipo: "contador", label: "Contador", img: "/images/Contador.png" },
    ]

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
                        <a href="/inicial/mapa/" className="hover:underline">Mapa</a>
                        <a href="#" className="hover:underline">Gráficos</a>
                        <a href="/inicial/exportacao/" className="hover:underline">Exportar</a>
                    </nav>
                </div>

                <button>
                    <img src="/images/UsuárioLogo.png" alt="Usuário" className="bg-none"></img>
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
                        <img src="/images/Usuário.png" alt="Avatar do Usuário" className="object-cover w-full h-full"></img>
                    </div>
                    <h2 className="text-white text-xl font-bold">Usuário</h2>
                </div>

                <nav className="flex flex-col gap-3">
                    <button onClick={()=> navigate("/inicial/crud/")} className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
                        Ambientes
                    </button>

                    <button onClick={()=> navigate("/inicial/crud")} className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
                        Sensores
                    </button>

                    <button onClick={()=> navigate("/inicial/historico")} className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
                        Histórico
                    </button>
                </nav>

                <button onClick={()=> navigate("/login/")} className="mt-auto flex items-center justify-center gap-2 border border-green-700 text-white text-xl px-4 py-2 rounded-md font-semibold transition-transform duration-1000 hover:scale-110">
                    <img src="/images/Botão Ícone - Sair.png" alt="Sair Ícone" className=" p-1 bg-green-700 rounded-full w-13 h-13"></img>
                    <span>Sair</span>
                </button>
            </aside>
        
                {/* Conteúdo Principal */}
        <main className="flex-1">
            <div className="min-h screen bg-gray-900 text-white p-8">
                <h1 className="text-3xl border border-green-700 rounded-full py-4 font-bold mb-8 text-center">Sensores Disponíveis</h1>

            {/* Card de Sensores */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-12">
                {sensores.map((sensor) => (
                    <div key={sensor.tipo} className="bg-gray-800 p-6 rounded-xl shadow hover:shadow-xl text-center">
                        <img src={sensor.img} alt={sensor.label} className="mx-auto mb-4 w-20 h-20"></img>
                        <h2 className="text-xl font-semibold mb-2">{sensor.label}</h2>
                        <p className="text-sm text-gray-300 mb-4">
                            Dados e valores captados recentemente pelo sensor de {sensor.label.toLowerCase()}.
                        </p>
                        <button
                        onClick={() => setSensorSelecionado(sensor.tipo)}
                        className="bg-green-700 hover:bg-green-700 text-white font-bold py-2 px-4">
                            Visualizar
                        </button>
                    </div>
                    
                ))}
            </div>

                {/* Gráfico */}
                <div className="bg-white p-6 rounded-lg shadow-md text-black">
                    <h2 className="text-2xl font-bold text-green-700 mb-4 capitalize">
                        Gráfico de {sensorSelecionado}
                    </h2>

                    <ResponsiveContainer width="100%" height={400}>
                        <LineChart data={dadosSensores[sensorSelecionado]}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis datakey="dia" />
                            <YAxis />
                            <Tooltip />
                            <Line
                            type="monotone"
                            dataKey="valor"
                            stroke="#22c55e"
                            strokeWidth={3}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
              </div>
            </main>
        </div>
        
        <footer className="bg-purple-800 text-white px-6 py-10 w-full">
        
                {/* Rodapé */}
        
              <div className="max-w-screen mx-auto flex flex-col lg:flex-row justify-between gap-10">
        
              <section className="flex-1">
                <h2 className="text-lg font-semibold mb-4">Envie o seu e-mail para mais notificações:</h2>
                <form className="flex items-center gap-2 mb-6">
                  <input
                  type="email"
                  placeholder="Seu e-mail"
                  className="p-2 rounded-md text-gray-800 w-full max-w-xs"
                  required
                  />
                  <button
                  type="submit"
                  className="bg-green-600 px-4 py-2 rounded-md hover:bg-green-600 transition">Enviar</button>
                </form>
                <div className="flex items-center gap-4 text-2xl">
                  <a href="#" aria-label="Instagram" className="hover:text-gray-300">
                    <FaInstagram/>
                  </a>
                  <a href="#" aria-label="Facebook" className="hover:text-gray-300">
                    <FaFacebook/>
                  </a>
                  <a href="#" aria-label="Linkedin" className="hover:text-gray-300">
                    <FaLinkedin/>
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
                  className="bg-green-600 px-4 py-2 rounded-md hover:bg-green-600 transition">Enviar</button>
                </form>
              </section>
             </div>
        
            <div className="mt-10 border-t border-purple-600 pt-6 text-sm text-center">
              <div className="flex flex-col lg:flex-row items-center justify-between gap-4 max-w-screen-xl mx-auto">
                <div className="flex items-center gap-2 justify-center">
                  <img 
                  src="/images/SmartCityLogo.png"
                  alt="SmartCity Logo"
                  className="w-12 h-12">
                  </img>
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
    )
};