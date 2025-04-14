from sagemaker.pytorch.model import PyTorchModel

model = PyTorchModel(
    model_data="s3://sagemaker-ap-south-1-590184109458/tts_models--en--ljspeech--glow-tts.tar.gz",  
    role="arn:aws:iam::590184109458:role/harshita-sagemaker-2",
    framework_version='2.5',
    py_version='py311',
    entry_point='serve.py',
    source_dir='new',
    env={
         "SAGEMAKER_REQUIREMENTS": "requirements.txt",
         
    }
)
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium',
    endpoint_name="kippss-tts"
)

print(predictor)
print(model)