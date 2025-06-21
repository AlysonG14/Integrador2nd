import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";

import { FaUser, FaLock } from "react-icons/fa6";
import { TfiEmail } from "react-icons/tfi";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const LoginSchema = z.object({
  email: z.string().email({ message: "Informe um novo email válido!" }),
  senha: z.string().length(8, { message: "Define uma senha de 8 caracteres!" }),
});

export function Login() {
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(LoginSchema) });

  function autenticarUsuario(data) {
    console.log(data);
    navigate("/inicial/")
  }
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100">
      <section className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 bg-white rounded-3xl shadow-2xl overflow-hidden">
        {/* Lado Esquerdo - Gradiente Roxo */}
        <div className="hidden md:block bg-gradient-to-br from-purple-900 via-purple-800 to-black rounded-l-3xl" />

        {/* Lado Direito - Formulário */}
        <div className="p-10 flex flex-col justify-center">
          <div className="text-center mb-6">
            <FaUser className="text-purple-800 mx-auto text-6xl" />
            <h1 className="text-3xl font-bold text-purple-800 mt-2">LOGIN</h1>
          </div>

          {/* Cadastro Social */}

          <form
            onSubmit={handleSubmit(autenticarUsuario)}
            className="space-y-4"
          >
            {/* Email */}

            <Input
              icon={<TfiEmail />}
              placeholder="Adicionar Email"
              error={errors.email?.message}
              register={register("email")}
              className="text-purple-800"
            />

            {/* Senha */}

            <Input
              icon={<FaLock />}
              type={mostrarSenha ? "text" : "password"}
              placeholder="Adicionar Senha"
              error={errors.senha?.message}
              register={register("senha")}
              rightIcon={
                mostrarSenha ? (
                  <FaEyeSlash
                    onClick={() => setMostrarSenha(false)}
                    className="cursor-pointer text-purple-800"
                  />
                ) : (
                  <FaEye
                    onClick={() => setMostrarSenha(true)}
                    className="cursor-pointer text-purple-800"
                  />
                )
              }
            />

            {/* Checkbox + Links */}
            <div className="flex items-center justify-between text-sm text-purple-800">
              <label className="flex items-center gap-2">
                <input type="checkbox" className="accent-purple-800" />
                Relembrar Senha
              </label>
              <span className="cursor-pointer underline hover:text-purple-600">
                Esqueceu a Senha?
              </span>
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-purple-800 text-white font-bold rounded-md hover:bg-purple-900 transition"
            >
              LOGIN
            </button>

            {/* Link para Cadasto */}

            <p
              className="text-center text-purple-800 underline cursor-pointer text-sm mt-2"
              onClick={() => navigate("/cadastro/")}
            >
              Cadastra-se
            </p>
          </form>
        </div>
      </section>
    </main>
  );
}

function Input({
  icon,
  placeholder,
  error,
  register,
  type = "text",
  rightIcon,
}) {
  return (
    <div>
      <div className="flex items-center border-2 border-purple-700 rounded px-3 py-2 bg-white">
        <div className="text-purple-700 mr-2">{icon}</div>
        <input
          type={type}
          placeholder={placeholder}
          {...register}
          className="flex-1 bg-transparent outline-none placeholder-purple-400 text-purple-900"
        />
        {rightIcon && <div className="ml-2">{rightIcon}</div>}
      </div>
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
}
