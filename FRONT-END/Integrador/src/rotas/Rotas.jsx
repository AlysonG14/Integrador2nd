import { BrowserRouter, Routes, Route } from "react-router-dom";

import { Login } from "../paginas/Login";
import { Cadastro } from "../paginas/Cadastro";
import { Mapa } from "../paginas/Mapa";
import { Exportacao } from "../paginas/Exportacao";
import { Historico } from "../paginas/Historico";
import { Grafico } from "../paginas/Grafico";
import { Inicial } from "../paginas/Inicial";
import { CRUD } from "../paginas/CRUD";


export function Rotas() {
  return (
    <BrowserRouter>
      <Routes>  
        <Route path="/login/" element={<Login/>}/>
        <Route path="/cadastro//" element={<Cadastro/>}/>
        <Route path="/inicial/" element={<Inicial/>}/>
        <Route path="/inicial/mapa/" element={<Mapa/>}/>
        <Route path="/inicial/exportacao/" element={<Exportacao/>}/>
        <Route path="/inicial/historico/" element={<Historico/>}/>
        <Route path="/inicial/grafico/" element={<Grafico/>}/>
        <Route path="/inicial/crud/" element={<CRUD/>}/>
      </Routes>
    </BrowserRouter>
  );
}
