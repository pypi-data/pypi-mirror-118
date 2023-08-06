# ERQA - Edge Restoration Quality Assessment

ERQA - a full-reference quality metric designed to analyze how good image and video restoration methods (SR, deblurring, denoising, etc) are restoring real details.

It is part of [MSU Video Super Resolution Benchmark](https://videoprocessing.ai/benchmarks/video-super-resolution.html) project.


## Quick start

Run `pip install erqa` and run it from command line or directly from Python code.

### Command line

```shell
python -m erqa /path/to/target.png /path/to/gt.png
```

### Python code

```python
import erqa
metric = erqa.ERQA()
v = metric(target, gt)
```

![](samples/erqa_vis.png)

## Local setup

You can get source code up and running using following commands:

```shell
git clone https://github.com/msu-video-group/erqa
cd erqa
pip install -r requirements.txt
```


TODO:
- [x] Requirements
- [x] Installation
- [ ] PyPi
- [ ] CI
- [ ] Cite us
- [x] Usage
- [x] Examples
- [x] Add license
