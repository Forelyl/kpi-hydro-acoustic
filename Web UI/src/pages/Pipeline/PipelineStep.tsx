import CloseIcon from '../../components/icons/CloseIcon';
import MenuIcon from '../../components/icons/MenuIcon';
import { IPipelineStep } from '../../hooks/usePipeline';
import AnalyzeTypeSelect from './AnalyzeTypeSelect';
import TimeBounds from './TimeBounds';
import TrackSelect from './TrackSelect';

interface Props {
  pipeline: IPipelineStep;
}

const PipelineStep = ({ pipeline }: Props) => {
  return (
    <div>
      <div>
        <MenuIcon />
        <div onClick={() => pipeline.removeSelf()}>
          <CloseIcon />
        </div>
        <TrackSelect />
        <AnalyzeTypeSelect />
      </div>
      <TimeBounds />
    </div>
  );
};

export default PipelineStep;
