const StatCard = ({ title, value, color }) => {
  return (
    <div
      className={`rounded-xl p-6 text-white shadow-md bg-gradient-to-r ${color}`}
    >
      <h3 className="text-lg font-medium">{title}</h3>
      <p className="text-4xl font-bold mt-3">{value}</p>
    </div>
  );
};

export default StatCard;
