// EventoLista.jsx
export default function EventoLista({ eventos }) {
  return (
    <div className="mt-8 space-y-4">
      {eventos.map((evento, index) => (
        <div
          key={index}
          className="evento-card" // aplica o estilo que você já definiu no App.css
        >
          <h2>{evento.nome}</h2>
          <p><strong>Data:</strong> {evento.data}</p>
          <p><strong>Organizador:</strong> {evento.organizador}</p>
          <p><strong>Palestrantes:</strong> {evento.palestrantes}</p>
          <p><strong>Patrocinadores:</strong> {evento.patrocinadores}</p>
          <p><strong>Participantes:</strong> {evento.participantes}</p>
        </div>
      ))}
    </div>
  );
}
