import CloseIcon from '../../../components/icons/CloseIcon';
import TrackSelect from '../TrackSelect';
import AnalyzeTypeSelect from '../AnalyzeTypeSelect';
import { IPipelineStep } from '../../../hooks/usePipeline';

interface Props {
  step: IPipelineStep;
}

const PipelineStepHeader = ({ step }: Props) => {
  return (
    <div
      className={`top_part ${
        step.analyzeType?.args.length ? '' : 'body_empty'
      }`}>
      <div>
        <div onClick={() => step.removeSelf()}>
          <CloseIcon />
        </div>
      </div>
      <div>
        {!!step.analyzeType?.choose_track && <TrackSelect step={step} />}
        <AnalyzeTypeSelect step={step} />
      </div>
    </div>
  );
};

export default PipelineStepHeader;
