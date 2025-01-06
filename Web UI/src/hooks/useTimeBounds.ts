import { ChangeEvent, useEffect, useMemo, useRef, useState } from 'react';
import { useAppSelector } from '../store/store';

const useTimeBounds = (onChange: (_: number) => void) => {
  const { fileDuration } = useAppSelector((state) => state.loadedFile);
  const [time, setTime] = useState({ minutes: 0, seconds: 0 });

  const secondRef = useRef<HTMLInputElement>(null);
  const minuteRef = useRef<HTMLInputElement>(null);

  const minutes = useMemo(() => {
    if (!time.minutes) return '00';
    if (time.minutes < 10) return `0${time.minutes}`;
    return time.minutes;
  }, [time]);

  const seconds = useMemo(() => {
    if (!time.seconds) return '00';
    if (time.seconds < 10) return `0${time.seconds}`;
    return time.seconds;
  }, [time]);

  useEffect(() => {
    onChange(+minutes * 60 + +seconds);
  }, [minutes, seconds, onChange]);

  const handleTimeChange =
    (type: 'minutes' | 'seconds') => (e: ChangeEvent<HTMLInputElement>) => {
      const maxMinutes = Math.floor(fileDuration / 60);
      const maxSeconds = time.minutes !== maxMinutes ? 59 : fileDuration % 60;

      if (type === 'minutes' && maxMinutes >= +e.target.value) {
        if (+e.target.value === maxMinutes)
          setTime((prev) => ({
            minutes: +e.target.value,
            seconds: Math.min(fileDuration % 60, prev.seconds)
          }));
        else setTime((prev) => ({ ...prev, minutes: +e.target.value }));

        if (minuteRef.current)
          minuteRef.current.value = minuteRef.current.value.replace(
            /^[0]/g,
            ''
          );
      }

      if (type === 'seconds' && maxSeconds >= +e.target.value) {
        setTime((prev) => ({ ...prev, seconds: +e.target.value }));

        if (secondRef.current)
          secondRef.current.value = secondRef.current.value.replace(
            /^[0]/g,
            ''
          );
      }
    };

  return {
    handleTimeChange,
    minuteRef,
    secondRef,
    minutes,
    seconds
  };
};

export default useTimeBounds;
