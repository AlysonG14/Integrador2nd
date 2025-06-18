import React from "react";
import styles from './LoginSchema.module.css'
import {useForm} from 'react-hook-form'
import {z} from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { BsPersonCircle } from "react-icons/bs";
import { FaKey } from "react-icons/fa6";

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
        <main>
            <div className={styles.container}>
                <div className={styles.nameIcon}>
                    <BsPersonCircle size={'80'} className={styles.userLogo}></BsPersonCircle>
                    <h1 className={styles.title}>Login</h1>
                    
                </div>
                    <div className={styles.register}>   
                        <p className={styles.email}>
                        Email</p>

                        <form
                            onSubmit={handleSubmit(autenticarUsuarioLogin)}
                            className={styles.form}>
                    
                            <div className={styles.fieldofLetter}>
                    
                            {errors.email && (<p>{errors.email.message}</p>)}

                            </div>
                            <input
                                {...register('email')} 
                                placeholder="Seu Email"
                                className={styles.field}>
                                </input>

                        <div className={styles.fieldofLetter}>

                </div>
                    </form>
                    <p className={styles.senha}>
                    Senha</p>
                    <form
                        onSubmit={handleSubmit(autenticarUsuarioLogin)}
                        className={styles.form}>
                        
                        <div className={styles.fieldofLetter}>
                        {errors.senha && (<p>{errors.senha.message}</p>)}

                        </div>
                        <input
                            {...register('senha')}
                            placeholder="Sua Senha"
                            className={styles.field}>
                        </input>

                        <br></br>
                        <div className={styles.componentsSenha}>
                            <a href={'/'}>Lembrar senha</a> <br></br>
                            <a href={'/'}>Esqueceu a senha</a>
                        </div>

                        <button to={'/inicial'}
                            className={styles.button}>Login
                        </button>
                        
                        <div className={styles.btn_add_user}>
                            <a href={'/cadastro'}>Cadastra-se</a>   
                        </div>

                    </form>

                </div>
                </div>
        </main>
    )

}