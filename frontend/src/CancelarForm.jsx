import { useState } from "react";

export default function CancelarForm({ API_URL, eventos, carregarEventos }) {
  const [cpfParticipante, setCpfParticipante] = useState("");
  const [idEvento, setIdEvento] = useState("");

  const cancelarInscricao = async (e) => {
    e.preventDefault();
    if (!cpfParticipante.trim() || !idEvento) return;

    const evento = eventos.find((ev) => ev.id === parseInt(idEvento));
    if (!evento) return;

    try {
      await fetch(`${API_URL}/cancelar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cpf_participante: cpfParticipante,
          nome_evento: evento.nome,
        }),
      });
      setCpfParticipante("");
      setIdEvento("");
      carregarEventos();
    } catch (err) {
      console.error("Erro ao cancelar inscrição", err);
    }
  };

  return (
    <form onSubmit={cancelarInscricao} className="flex flex-col gap-2 max-w-xl mx-auto mb-6 p-4 bg-gray-800 rounded">
      <h2 className="font-semibold text-xl mb-2">Cancelar Inscrição</h2>
      <input type="text" value={cpfParticipante} onChange={(e) => setCpfParticipante(e.target.value)} placeholder="CPF do participante" className="p-2 rounded text-black" />
      <input type="number" value={idEvento} onChange={(e) => setIdEvento(e.target.value)} placeholder="ID do evento" className="p-2 rounded text-black" />
      <button className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded">Cancelar</button>
    </form>
  );
}