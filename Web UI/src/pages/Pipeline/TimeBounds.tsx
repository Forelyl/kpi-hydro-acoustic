import { useAppSelector } from '../../store/store';

const TimeBounds = () => {
  const { fileDurationString } = useAppSelector((state) => state.loadedFile);

  return (
    <div>
      <div>
        <label htmlFor="start-time">Start time 00:00</label>
        <div>
          <input id="start-time" type="time" required />
        </div>
      </div>
      <div>
        <label htmlFor="end-time">End time {fileDurationString}</label>
        <div>
          <input id="end-time" type="time" required />
        </div>
      </div>
    </div>
  );
};

export default TimeBounds;
