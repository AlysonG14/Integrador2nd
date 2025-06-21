import React from "react";
import {FaInstagram, FaFacebook, FaLinkedin,} from "react-icons/fa";

export function Rodapé() {
  return (
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
            <a href="#" aria-label="Instagram" className="hover:text-gray-300">
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
              src="images/SmartCityLogo.png"
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
  );
}
