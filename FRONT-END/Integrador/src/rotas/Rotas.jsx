import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LoginSchema } from '../paginas/LoginSchema';
import { Cadastro } from '../paginas/Cadastro';
import { Exportar } from '../paginas/Exportar';
import { Home } from '../paginas/Home';

export function Rotas() {
    return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginSchema />} />
        <Route path="/cadastro" element={<Cadastro />} />
          <Route path="/inicial" element={<Home />}>
          <Route path="/exportar" element={<Exportar />} />
        </Route>
      </Routes>
    </BrowserRouter>
    );
}