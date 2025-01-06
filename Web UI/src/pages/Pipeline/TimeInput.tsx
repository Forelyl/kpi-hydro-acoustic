import useTimeBounds from '../../hooks/useTimeBounds';

interface Props {
  onChange: (_: number) => void;
}

const TimeInput = ({ onChange }: Props) => {
  const { minutes, seconds, minuteRef, secondRef, handleTimeChange } =
    useTimeBounds(onChange);

  return (
    <div className="time-input-wrapper">
      <input
        ref={minuteRef}
        className="time-input"
        id="start-time"
        required
        type="number"
        onChange={handleTimeChange('minutes')}
        value={minutes}
      />
      :
      <input
        ref={secondRef}
        className="time-input"
        id="start-time"
        required
        type="number"
        onChange={handleTimeChange('seconds')}
        value={seconds}
      />
    </div>
  );
};

export default TimeInput;
