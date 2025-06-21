import React from "react";
import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { Icon } from "leaflet";
import { FaUser } from "react-icons/fa";
import {FaInstagram, FaFacebook, FaLinkedin,} from "react-icons/fa";

const redIcon = new Icon({
  iconUrl: "/images/Vermelho.png",
  iconSize: [30, 42],
  iconAnchor: [15, 42],
});

const blueIcon = new Icon({
  iconUrl: "/images/Azul.png",
  iconSize: [30, 42],
  iconAnchor: [15, 42],
});

const sensores = [
  { id: 1, nome: "Washington", lat: 38.89511, lng: -77.03637, cor: "red" },
  { id: 2, nome: "Baltimore", lat: 39.2904, lng: -76.6122, cor: "red" },
  { id: 3, nome: "Alexandria", lat: 38.8048, lng: -77.0469, cor: "blue" },
  { id: 4, nome: "Germantown", lat: 39.1732, lng: -77.2716, cor: "blue" },
  { id: 5, nome: "Dale City", lat: 38.6376, lng: -77.3111, cor: "blue" },
  { id: 6, nome: "Annapolis", lat: 38.9784, lng: -76.4922, cor: "blue" },
  { id: 7, nome: "Waldorf", lat: 38.6246, lng: -76.9391, cor: "blue" },
  { id: 8, nome: "Silver Spring", lat: 39.0068, lng: -77.0301, cor: "blue" },
];

export function Mapa() {
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
            <a href="#" className="hover:underline">
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
            alt="UsuárioLogo"
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

            <button onClick={()=> navigate("/inicial/crud")} className="border border-green-700 text-white text-xl py-2 rounded-lg font-semibold transition-transform duration-1000 hover:scale-110">
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

        {/* Barra de Pesquisa */}

        <main className="flex-1">
          <section className="p-8">
            <div className="bg-gray-100 border border-gray-300 rounded-[4px] p-1 overflow-hidden shadow-md">
              <div className="bg-gray-300 p-3 flex items-center gap-2">
                <label htmlFor="pesquisaMapa" className="sr-only">
                  Pesquisar Localização
                </label>
                <input
                  id="pesquisaMapa"
                  type="text"
                  placeholder="Pesquisar"
                  className="flex-1 px-3 py-2 rounded-sm bg-white border border-gray-400 text-gray-800 text-sm focus:outline none"
                />
                <img
                  src="/images/Lupa.png"
                  alt="Buscar"
                  className="w-5 h-5"
                ></img>
              </div>

              {/* Mapa */}

              <MapContainer
                center={[38.89511, -77.03637]}
                zoom={9}
                scrollWheelZoom={true}
                className="h-[600px] w-full"
              >
                <TileLayer
                  url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                  attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
                />
                {sensores.map((s) => (
                  <Marker
                    key={s.id}
                    position={[s.lat, s.lng]}
                    icon={s.cor === "red" ? redIcon : blueIcon}
                  >
                    <Popup>
                      <strong>{s.nome}</strong>
                    </Popup>
                  </Marker>
                ))}
              </MapContainer>
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
