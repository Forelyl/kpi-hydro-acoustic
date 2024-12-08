const AnalyzeTypeSelect = () => {
  const analizeTypes = ['a', 'b', 'c'];

  return (
    <select defaultValue="Analyze type">
      <option hidden>Analyze type</option>
      {analizeTypes.map((type, index) => (
        <option key={index} value={type}>
          {type}
        </option>
      ))}
    </select>
  );
};

export default AnalyzeTypeSelect;
