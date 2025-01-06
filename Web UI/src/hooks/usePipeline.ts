import { useCallback, useMemo, useState } from 'react';
import { IAnalyzeType } from '../store/pipelineApi';

export interface IPipelineStep {
  id: number;
  analyzeType?: IAnalyzeType;
  track?: number;
  data?: unknown[];
  setAnalyzeType: (_: IAnalyzeType) => void;
  setTrack: (_: number) => void;
  setData: (_: unknown[]) => void;
  removeSelf: () => void;
}

const usePipeline = () => {
  const handleRemoveStep = useCallback(
    (id: number) => () => {
      setPipeline((prev) => prev.filter((pipeline) => pipeline.id !== id));
    },
    []
  );

  const handleSelectAnalyzeType = useCallback(
    (id: number) => (type: IAnalyzeType) => {
      setPipeline((prev) =>
        prev.map((step) => {
          if (step.id === id) step.analyzeType = type;
          return step;
        })
      );
    },
    []
  );

  const handleSelectTrack = useCallback(
    (id: number) => (track: number) => {
      setPipeline((prev) =>
        prev.map((step) => {
          if (step.id === id) step.track = track;
          return step;
        })
      );
    },
    []
  );

  const handleSetData = useCallback(
    (id: number) => (data: unknown[]) => {
      setPipeline((prev) =>
        prev.map((step) => {
          if (step.id === id) step.data = data;
          return step;
        })
      );
    },
    []
  );

  const defaultStep: IPipelineStep = useMemo(
    () => ({
      id: 0,
      removeSelf: handleRemoveStep(0),
      setAnalyzeType: handleSelectAnalyzeType(0),
      setTrack: handleSelectTrack(0),
      setData: handleSetData(0)
    }),
    [
      handleRemoveStep,
      handleSelectAnalyzeType,
      handleSelectTrack,
      handleSetData
    ]
  );

  const handleAddStep = useCallback(() => {
    setPipeline((prev) => {
      const newStep = { ...defaultStep };
      newStep.id = Date.now();
      newStep.removeSelf = handleRemoveStep(newStep.id);
      newStep.setAnalyzeType = handleSelectAnalyzeType(newStep.id);
      newStep.setTrack = handleSelectTrack(newStep.id);
      newStep.setData = handleSetData(newStep.id);
      return [...prev, newStep];
    });
  }, [
    defaultStep,
    handleRemoveStep,
    handleSelectAnalyzeType,
    handleSelectTrack,
    handleSetData
  ]);

  const [pipeline, setPipeline] = useState<IPipelineStep[]>([defaultStep]);

  return { pipeline, handleAddStep };
};

export default usePipeline;
