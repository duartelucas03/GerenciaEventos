import { useState } from "react";

export default function InscricaoForm({ API_URL, carregarEventos }) {
  const [cpfParticipante, setCpfParticipante] = useState("");
  const [idEvento, setIdEvento] = useState("");

  const inscreverParticipante = async (e) => {
    e.preventDefault();
    if (!cpfParticipante.trim() || !idEvento) return;

    try {
      await fetch(`${API_URL}/inscrever`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cpf_participante: cpfParticipante,
          id_evento: parseInt(idEvento),
        }),
      });
      setCpfParticipante("");
      setIdEvento("");
      carregarEventos();
    } catch (err) {
      console.error("Erro ao inscrever participante", err);
    }
  };

  return (
    <form onSubmit={inscreverParticipante} className="flex flex-col gap-2 max-w-xl mx-auto mb-6 p-4 bg-gray-800 rounded">
      <h2 className="font-semibold text-xl mb-2">Inscrever Participante</h2>
      <input type="text" value={cpfParticipante} onChange={(e) => setCpfParticipante(e.target.value)} placeholder="CPF do participante" className="p-2 rounded text-black" />
      <input type="number" value={idEvento} onChange={(e) => setIdEvento(e.target.value)} placeholder="ID do evento" className="p-2 rounded text-black" />
      <button className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded">Inscrever</button>
    </form>
  );
}