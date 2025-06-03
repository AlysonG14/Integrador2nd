import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Cadastro } from '../paginas/Cadastro';
import { Exportar } from '../paginas/Exportar';
import { Home } from '../paginas/Home';

export function Rotas() {
    return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Cadastro />} />
        <Route path="home" element={<Home />}>
          <Route path="exportar" element={<Exportar />} />
        </Route>
      </Routes>
    </BrowserRouter>
    );
}