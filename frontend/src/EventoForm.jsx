import { useState } from "react";

export default function EventoForm({ API_URL, carregarEventos }) {
  const [nomeEvento, setNomeEvento] = useState("");
  const [cpfOrganizador, setCpfOrganizador] = useState("");
  const [cpfsPalestrantes, setCpfsPalestrantes] = useState("");
  const [cnpjsPatrocinadores, setCnpjsPatrocinadores] = useState("");

  const criarEvento = async (e) => {
    e.preventDefault();
    if (!nomeEvento.trim() || !cpfOrganizador.trim()) return;

    try {
      await fetch(`${API_URL}/eventos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nome: nomeEvento,
          cpf_organizador: cpfOrganizador,
          cpfs_palestrantes: cpfsPalestrantes
            ? cpfsPalestrantes.split(",").map((c) => c.trim())
            : [],
          cnpjs_patrocinadores: cnpjsPatrocinadores
            ? cnpjsPatrocinadores.split(",").map((c) => c.trim())
            : [],
        }),
      });
      setNomeEvento("");
      setCpfOrganizador("");
      setCpfsPalestrantes("");
      setCnpjsPatrocinadores("");
      carregarEventos();
    } catch (err) {
      console.error("Erro ao criar evento", err);
    }
  };

  return (
    <form onSubmit={criarEvento} className="flex flex-col gap-2 max-w-xl mx-auto mb-6 p-4 bg-gray-800 rounded">
      <h2 className="font-semibold text-xl mb-2">Criar Evento</h2>
      <input type="text" value={nomeEvento} onChange={(e) => setNomeEvento(e.target.value)} placeholder="Nome do evento" className="p-2 rounded text-black" />
      <input type="text" value={cpfOrganizador} onChange={(e) => setCpfOrganizador(e.target.value)} placeholder="CPF do organizador" className="p-2 rounded text-black" />
      <input type="text" value={cpfsPalestrantes} onChange={(e) => setCpfsPalestrantes(e.target.value)} placeholder="CPFs dos palestrantes (vírgula)" className="p-2 rounded text-black" />
      <input type="text" value={cnpjsPatrocinadores} onChange={(e) => setCnpjsPatrocinadores(e.target.value)} placeholder="CNPJs dos patrocinadores (vírgula)" className="p-2 rounded text-black" />
      <button className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">Criar Evento</button>
    </form>
  );
}