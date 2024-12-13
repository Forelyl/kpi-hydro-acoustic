import { useState } from 'react';
import TimeInput from './TimeInput';

const TimeBounds = () => {
  const [startTime, setStartTime] = useState<number>(0);
  const [endTime, setEndTime] = useState<number>(0);

  return (
    <div className="fields_container">
      <div className="time_select">
        <div className="label_box">
          <label htmlFor="start-time">Start time</label>
          <TimeInput onChange={setStartTime} />
        </div>
      </div>
      <div className="time_select">
        <div className="label_box">
          <label htmlFor="end-time">End time</label>
          <TimeInput onChange={setEndTime} />
        </div>
      </div>
      {endTime < startTime ? <span>Ti eblan</span> : ''}
    </div>
  );
};

export default TimeBounds;
