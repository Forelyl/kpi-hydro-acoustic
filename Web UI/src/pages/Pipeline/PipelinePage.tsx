import PipelineStep from './PipelineStep/PipelineStep';
import usePipeline from '../../hooks/usePipeline';
import PlusIcon from '../../components/icons/PlusIcon';
import SendIcon from '../../components/icons/SendIcon';
import { useSendPipelineMutation } from '../../store/pipelineApi';
import { useAppDispatch, useAppSelector } from '../../store/store';
import { useNavigate } from 'react-router';
import {
  resetError,
  setError,
  setResultZip
} from '../../store/loadedFileSlice';
import Modal from '../../components/Modal/Modal';
import { pipelineErrors } from '../../errors/pipelineErrors';

const Pipeline = () => {
  const { pipeline, handleAddStep } = usePipeline();
  const [sendPipeline, { isLoading }] = useSendPipelineMutation();
  const { file, separateTracks, error } = useAppSelector(
    (state) => state.loadedFile
  );
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const handleSendPipeline = () => {
    const steps = pipeline.map((step) => ({
      id: step.analyzeType?.id,
      track: [step.track],
      args: step.data
    }));

    for (const step of steps) {
      if (!step.track[0]) {
        dispatch(setError(pipelineErrors.NO_TRACK_SELECTED));
        return;
      }
    }

    const formData = new FormData();

    formData.append('file', file!);
    formData.append('separate', `${separateTracks}`);
    formData.append('pipeline', `{"pipeline": ${JSON.stringify(steps)}}`);

    sendPipeline(formData)
      .unwrap()
      .then((res) => {
        dispatch(setResultZip(res as Blob));
        void navigate('/download');
      })
      .catch(console.error);
  };
  return (
    <main id="pipline_page">
      {pipeline.map((step) => (
        <PipelineStep step={step} key={step.id} />
      ))}

      <div onClick={handleAddStep} className="add_step">
        <PlusIcon />
      </div>
      <div onClick={handleSendPipeline} className="add_step">
        <SendIcon />
      </div>
      <Modal open={!!error}>
        <h2>{error?.title}</h2>
        <p>{error?.message}</p>
        <button onClick={() => dispatch(resetError())}>OK</button>
      </Modal>
      {isLoading ? (
        <div>
          <h3>Analyzing...</h3>
        </div>
      ) : (
        <></>
      )}
    </main>
  );
};

export default Pipeline;
