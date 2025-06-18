import React from "react";
import { useForm } from "react-hook-form"
import { z } from 'zod'
import { zodResolver } from "@hookform/resolvers/zod"; 

import { BsPersonCircle } from "react-icons/bs";
import { FaUser } from "react-icons/fa6";
import { GiEarthAmerica } from "react-icons/gi";
import { BsTelephonePlus } from "react-icons/bs";
import { TfiEmail } from "react-icons/tfi";
import { FaLock } from "react-icons/fa";
import { FaLockOpen } from "react-icons/fa";


const cadastroSchema = z.object({
    usuario: z.string().min(1, {message: 'Informe um novo usuário correto!'}),
    pais: z.string().min(1, {message: 'Informe um novo país válido!'}),
    telefone: z.string().min(10, {message: 'Informe um novo telefone válido!'}).max(15),
    email: z.string().email({message: 'Informe um novo email válido!'}),
    senha: z.string().length(8, {message: 'Define uma senha de 8 caracteres!'}),
    confirmarSenha: z.string().length(8, {message: 'Define uma senha de 8 caracteres!'}),
}).refine((data => data.senha === data.confirmarSenha), {
  message: 'As senhas não coincidem!',
  path: ['confirmarSenha'],
});

export function CadastroSchema(){
    const {register,
      handleSubmit,
      formState: {errors
    }} = useForm({resolver: zodResolver(cadastroSchema)})

    function autenticarUsuarioCadastro(data){
      console.log(data.usuario)
      console.log(data.pais)
      console.log(data.telefone)
      console.log(data.email)

    }
    return(
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-r from-white via-purple-100 to-purple-300">
        <div className="bg-white shadow-lg rounded-2xl w-full max-w-md p-8">
          <div className="flex flex-col items-center mb-6">
            <BsPersonCircle size={80} className="text-purple-700"/>
            <h1 className="mt-4 text-2xl font-bold text-purple-900">Cadastro</h1>
          </div>

          {/* Login Social */}

          

          <form onSubmit={handleSubmit(autenticarUsuarioCadastro)} className="space-y-4">

            {/* Usuário */}

            <div className="flex items-center border-2 border-purple-700 rounded px-3 py-2">
              <FaUser className="text-purple-700 mr-2"/>
              <input type="text" placeholder="Novo Usuário" {...register("usuario")} className="flex-1 bg-transparent outline-none placeholder-purple-400" />
              {errors.usuario && <p className="text-sm text-purple-700">{errors.usuario.message}</p>}
            </div>

            {/* País */}

            <div className="flex items-center border-2 border-purple-700 rounded px-3 py-2">
              <GiEarthAmerica className="text-purple-700 mr-2"/>
              <input type="text" placeholder="Adicionar País" {...register("pais")} className="flex-1 bg-transparent outline-none placeholder-purple-400" />
              {errors.pais && <p className="text-sm text-purple-700">{errors.pais.message}</p>}
            </div>

            {/* Telefone */}

            <div className="flex items-center border-2 border-purple-700 rounded px-3 py-2">
              <BsTelephonePlus className="text-purple-700 mr-2"/>
              <input type="text" placeholder="Adicionar Telefone"{...register("telefone")} className="flex-1 bg-transparent outline-none placeholder-purple-400" />
              {errors.telefone && <p className="text-sm text-purple-700">{errors.telefone.message}</p>}
            </div>

            {/* Email */}

            <div className="flex items-center border-2 border-purple-700 rounded px-3 py-2">
              <TfiEmail className="text-purple-700 mr-2"/>
              <input type="text" placeholder="Adicionar Email"{...register("email")} className="flex-1 bg-transparent outline-none placeholder-purple-400" />
              {errors.email && <p className="text-sm text-purple-700">{errors.email.message}</p>}
            </div>

            {/* Senha */}

            <div className="flex items-center border-2 border-purple-700 rounded px-3 py-2">
              <FaLock className="text-purple-700 mr-2"/>
              <input type="password" placeholder="Nova Senha"{...register("senha")} className="flex-1 bg-transparent outline-none placeholder-purple-400" />
              {errors.senha && <p className="text-sm text-purple-700">{errors.senha.message}</p>}
            </div>

            {/* Confirmar Senha */}

            <div className="flex items-center border-2 border-purple-700 rounded px-3 py-2">
              <FaLockOpen className="text-purple-700 mr-2"/>
              <input type="password" placeholder="Confirmar Senha" {...register("confirmarSenha")} className="flex-1 bg-transparent outline-none placeholder-purple-400" />
              {errors.confirmarSenha && <p className="text-sm text-purple-700">{errors.confirmarSenha.message}</p>}
            </div>

            <button type="submit" className="w-full mt-2 py-2 bg-purple-700 hover:bg-purple-800 text-white rounded font-semibold transition-colors">
              CADASTRAR
            </button>

            {/* Link para Login */}

            <div>
              <a href="#" className="text-sm text-purple-700 underline">Fazer Login</a>
            </div>

          </form>
        </div>
      </main>
    );
}

