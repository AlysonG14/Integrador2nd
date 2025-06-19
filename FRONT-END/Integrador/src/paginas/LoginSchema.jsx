import React from "react";
import {useForm} from 'react-hook-form'
import {z} from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { BsPersonCircle } from "react-icons/bs";
import { TfiEmail } from "react-icons/tfi";
import { FaLock } from "react-icons/fa6";

const loginSchema = z.object({
    email: z.string().email({message: 'Informe um e-mail válido!'}),
    senha: z.string().length(8, {message: 'Define uma senha de 8 caracteres!'})
})

export function LoginSchema(){

    const {register,
        handleSubmit,
        formState: {errors
        }} = useForm({resolver: zodResolver(loginSchema)})

    function autenticarUsuarioLogin(data){
        console.log(data.email)
        console.log(data.senha)
    }
    return(
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-r from-white via-purple-100 to-purple-300">
        <div className="bg-white shadow-lg rounded-2xl w-full max-w-md p-8">
          <div className="flex flex-col items-center mb-6">
            <BsPersonCircle size={80} className="text-purple-700"/>
            <h1 className="mt-4 text-2xl font-bold text-purple-900">Login</h1>
          </div>

          <form onSubmit={handleSubmit(autenticarUsuarioLogin)} className="space-y-4">

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

            <div>
                <button type="checkbox" className=""></button>
                <a href='#'>Relembrar Senha</a>
                <a href='#'>Esqueceu a Senha?</a>
            </div>

            <button type="submit" className="w-full mt-2 py-2 bg-purple-700 hover:bg-purple-800 text-white rounded font-semibold transition-colors">
              LOGIN
            </button>

            {/* Link para Cadastro */}

            <div>
              <a href="#" className="text-sm text-purple-700 underline">Cadastro</a>
            </div>

          </form>
        </div>
      </main>
    );
}
