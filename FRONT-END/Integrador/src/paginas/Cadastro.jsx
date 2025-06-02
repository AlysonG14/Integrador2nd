import React from "react";
import styles from './Cadastro.module.css'
import {useForm} from 'react-hook-form'
import {z} from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { BsPersonCircle } from "react-icons/bs";
import { FaKey } from "react-icons/fa6";

const loginSchema = z.object({
    email: z.string().email({message: 'Informe um e-mail válido!'}),
    senha: z.string().length(8, {message: 'Define uma senha de 8 caracteres!'})
})

export function Cadastro(){

    const {register,
        handleSubmit,
        formState: {errors
        }} = useForm({resolver: zodResolver(loginSchema)})

    function autenticarUsuario(data){
        console.log(data.email)
        console.log(data.senha)
    }
    
    return(
        <div className={styles.container}>
            <div className={styles.nameIcon}>
                    <h1 className={styles.title}>Login</h1>
                </div>
                    <div className={styles.register}>   
                    <p className={styles.title}> <BsPersonCircle size={'40'} className={styles.icon} />
                    Email </p>

                    <form
                        onSubmit={handleSubmit(autenticarUsuario)}
                        className={styles.form}>
                    
                        <div className={styles.fieldofLetter}>
                    
                        {errors.email && (<p>{errors.email.message}</p>)}

                        </div>
                        <input
                            {...register('email')}
                            placeholder="E-mail"
                            className={styles.field}>
                            </input>

                        <div className={styles.fieldofLetter}>

                </div>
                    </form>


                    <p className={styles.title}> <FaKey size={'40'} className={styles.icon} />
                    Password </p>
                    <form
                        onSubmit={handleSubmit(autenticarUsuario)}
                        className={styles.form}>
                        
                        <div className={styles.fieldofLetter}>
                        {errors.senha && (<p>{errors.senha.message}</p>)}

                        </div>
                        <input
                            {...register('senha')}
                            placeholder="Senha"
                            className={styles.field}>
                        </input>

                        <button to={'/inicial'}
                            className={styles.button}>Enter
                        </button>

                    </form>

                </div>
                </div>
    )

}