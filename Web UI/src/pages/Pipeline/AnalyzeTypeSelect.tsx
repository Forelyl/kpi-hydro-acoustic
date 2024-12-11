import SelectOpenIcon from '../../components/icons/SelectOpenIcon';

const AnalyzeTypeSelect = () => {
  const analizeTypes = ['a', 'b', 'c'];

  return (
    <div className="select_container type_select">
      <select defaultValue="Analyze type" className="select ">
        <option hidden>Analyze type</option>
        {analizeTypes.map((type, index) => (
          <option key={index} value={type}>
            {type}
          </option>
        ))}
      </select>
      <div className='image_container'>
        <SelectOpenIcon />
      </div>
    </div>
  );
};

export default AnalyzeTypeSelect;
