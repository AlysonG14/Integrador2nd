import React from 'react';
import styles from './Exportar.module.css';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { FaUserCircle } from "react-icons/fa";


export function Exportar(){
    return (
        <div className={styles.container} >
            <div className={styles.bar} >
                <a href=''>About</a>
                <a href=''>Dashboard</a>
                <a href=''>Home</a>
                <FaUserCircle size={'40'}></FaUserCircle>
            </div>
        </div>
    )
}