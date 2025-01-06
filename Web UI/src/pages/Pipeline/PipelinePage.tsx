import PipelineStep from './PipelineStep/PipelineStep';
import usePipeline from '../../hooks/usePipeline';
import PlusIcon from '../../components/icons/PlusIcon';
import SendIcon from '../../components/icons/SendIcon';

const Pipeline = () => {
  const { pipeline, handleAddStep } = usePipeline();

  const handleSendPipeline = () => {
    const toSend = pipeline.map((step) => ({
      id: step.analyzeType?.id,
      track: [step.track],
      args: step.data
    }));
    console.log(toSend);
  };

  return (
    <main id="pipline_page">
      {pipeline.map((step) => (
        <PipelineStep step={step} key={step.id} />
      ))}

      <div onClick={handleAddStep} id="add_step">
        <PlusIcon />
      </div>
      <div onClick={handleSendPipeline} id="add_step">
        <SendIcon />
      </div>
    </main>
  );
};

export default Pipeline;
