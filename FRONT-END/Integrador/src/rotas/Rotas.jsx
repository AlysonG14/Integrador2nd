import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LoginSchema } from '../paginas/LoginSchema';
import { CadastroSchema } from '../paginas/CadastroSchema';
import { Exportar } from '../paginas/Exportar';
import { Home } from '../paginas/Home';

export function Rotas() {
    return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginSchema />} />
        <Route path="/cadastro" element={<CadastroSchema />} />
          <Route path="/inicial" element={<Home />}>
          <Route path="/exportar" element={<Exportar />} />
        </Route>
      </Routes>
    </BrowserRouter>
    );
}