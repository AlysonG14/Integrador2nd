import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

import { FaUserPlus } from "react-icons/fa6";
import { BsTelephonePlus } from "react-icons/bs";
import { FaUser, FaLock } from "react-icons/fa6";
import { FaLockOpen } from "react-icons/fa";
import { TfiEmail } from "react-icons/tfi";
import { GiEarthAmerica } from "react-icons/gi";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { FaFacebookF } from "react-icons/fa";
import { FcGoogle } from "react-icons/fc";
import { FaLinkedinIn } from "react-icons/fa";

const cadastroSchema = z
  .object({
    usuario: z.string().min(1, { message: "Informe um novo usuário correto!" }),
    pais: z.string().min(1, { message: "Informe um novo país válido!" }),
    telefone: z
      .string()
      .min(10, { message: "Informe um novo telefone válido!" })
      .max(15),
    email: z.string().email({ message: "Informe um novo email válido!" }),
    senha: z
      .string()
      .length(8, { message: "Define uma senha de 8 caracteres!" }),
    confirmarSenha: z
      .string()
      .length(8, { message: "Define uma senha de 8 caracteres!" }),
  })
  .refine((data) => data.senha === data.confirmarSenha, {
    message: "As senhas não coincidem!",
    path: ["confirmarSenha"],
  });

export function Cadastro() {
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [mostrarConfirmar, setMostrarConfirmar] = useState(false);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(cadastroSchema) });

  function autenticarUsuarioCadastro(data) {
    console.log(data);
    navigate("/login/");
  }
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100">
      <section className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 bg-white rounded-3xl shadow-2xl overflow-hidden">
        {/* Lado Esquerdo - Formulário */}

        <div className="p-10">
          <div className="text-center mb-6">
            <FaUserPlus className="text-purple-800 mx-auto text-6xl" />
            <h1 className="text-3xl font-bold text-purple-800 mt-2">
              CADASTRO
            </h1>
          </div>

          {/* Botões Sociais */}
          <div className="flex justify-center gap-4 mb-6">
            <button className="bg-gray-200 p-3 rounded-full hover:shadow-md">
              <FaLinkedinIn className="text-xl text-blue-800" />
            </button>
            <button className="bg-gray-200 p-3 rounded-full hover:shadow-md">
              <FcGoogle className="text-xl" />
            </button>
            <button className="bg-gray-200 p-3 rounded-full hover:shadow-md">
              <FaFacebookF className="text-xl text-blue-600" />
            </button>
          </div>

          {/* Cadastro Social */}

          <form
            onSubmit={handleSubmit(autenticarUsuarioCadastro)}
            className="space-y-4"
          >
            {/* Usuário */}

            <Input
              icon={<FaUser />}
              placeholder="Novo Usuário"
              error={errors.usuario?.message}
              register={register("usuario")}
              className="text-purple-800"
            />

            {/* País */}

            <Input
              icon={<GiEarthAmerica />}
              placeholder="Adicionar País"
              error={errors.pais?.message}
              register={register("pais")}
              className="text-purple-800"
            />

            {/* Telefone */}

            <Input
              icon={<BsTelephonePlus />}
              placeholder="Adicionar Telefone"
              error={errors.telefone?.message}
              register={register("telefone")}
              className="text-purple-800"
            />

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
              error={errors.usuario?.message}
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

            {/* Confirmar Senha */}

            <Input
              icon={<FaLockOpen />}
              type={mostrarConfirmar ? "text" : "password"}
              placeholder="Confirmar Senha"
              error={errors.usuario?.message}
              register={register("confirmarSenha")}
              rightIcon={
                mostrarConfirmar ? (
                  <FaEyeSlash
                    onClick={() => setMostrarConfirmar(false)}
                    className="cursor-pointer text-purple-800"
                  />
                ) : (
                  <FaEye
                    onClick={() => setMostrarConfirmar(true)}
                    className="cursor-pointer text-purple-800"
                  />
                )
              }
            />

            <button
              type="submit"
              className="w-full py-3 bg-purple-800 text-white font-bold rounded-md hover:bg-purple-800 transition"
            >
              CADASTRAR
            </button>

            {/* Link para Login */}

            <p
              className="text-center text-purple-800 underline cursor-pointer text-sm mt-2"
              onClick={() => navigate("/login/")}
            >
              Fazer Login
            </p>
          </form>
        </div>

        {/* Lado Direito - Imagem de Fundo Roxo */}

        <div className="hidden md:block bg-gradient-to-br from-purple-900 via-purple-800 to-black" />
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
          className="flex-1 bg-transparent outline-none placeholder-purple-400"
        />
        {rightIcon && <div className="ml-2">{rightIcon}</div>}
      </div>
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
}
