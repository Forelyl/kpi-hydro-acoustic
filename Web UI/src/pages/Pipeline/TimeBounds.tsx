import { useAppSelector } from '../../store/store';

const TimeBounds = () => {
  const { fileDurationString } = useAppSelector((state) => state.loadedFile);

  return (
    <div className='fields_container'>
      <div className='time_select'>
        <div className='label_box'>
          <label htmlFor="start-time">Start time</label>
        </div>
        <input id="start-time" type="time" defaultValue={"00:00"}  required />
      </div>
      <div className='time_select'>
        <div className='label_box'>
          <label htmlFor="end-time">End time</label>
        </div>
          <input id="end-time" type="time" defaultValue={fileDurationString} required />
      </div>
    </div>
  );
};

export default TimeBounds;
