import { useEffect, useState } from "react";
import EventoForm from "./EventoForm";
import InscricaoForm from "./InscricaoForm";
import CancelarForm from "./CancelarForm";
import EventoLista from "./EventoLista";
import "./App.css";

export default function App() {
  const [eventos, setEventos] = useState([]);
  const API_URL = "http://localhost:8000"; // ajuste conforme necessÃ¡rio

  const carregarEventos = async () => {
    try {
      const res = await fetch(`${API_URL}/eventos`);
      if (!res.ok) throw new Error("Erro ao buscar eventos");
      const data = await res.json();
      setEventos(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    carregarEventos();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">Gerenciador de Eventos</h1>

      <EventoForm API_URL={API_URL} carregarEventos={carregarEventos} />
      <InscricaoForm API_URL={API_URL} carregarEventos={carregarEventos} />
      <CancelarForm API_URL={API_URL} eventos={eventos} carregarEventos={carregarEventos} />
      <EventoLista eventos={eventos} />
    </div>
  );
}

