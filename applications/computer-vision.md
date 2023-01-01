
# Computer vision

Not actually an application, more like an entire application domain.

Motivation: 

"Recent studies show that the latencies to upload
a JPEG-compressed input image (i.e. 152KB) for a single inference
of a popular CNN–“AlexNet” via stable wireless connections with
3G (870ms), LTE (180ms) and Wi-Fi (95ms), can exceed that of DNN
computation (6∼82ms) by a mobile or cloud-GPU."
Moreover,the communication energy is comparable with the associated DNN computation energy.

Y. Kang, J. Hauswald, C. Gao, A. Rovinski, T. Mudge, J. Mars, and L. Tang,
“Neurosurgeon: Collaborative intelligence between the cloud and mobile edge,”
in Proceedings of the Twenty-Second International Conference on Architectural Support
for Programming Languages and Operating Systems. ACM, 2017, pp. 615–629.

## Tools

* [VLFeat](http://www.vlfeat.org/api/index.html).
Portable C library with lots of feature extractors for computer vision tasks.


### Classifying JPEG-compressed data

Can one do classification and object detection on compressed JPEG straight from the camera?
Instead of computing the framebuffer from the JPEG.

Can it be also done in a streaming fashion?

Operating on the blocks with DCT coefficients.

Prior work:

- [Faster Neural Networks Straight from JPEG](https://openreview.net/forum?id=S1ry6Y1vG).
ICL2018. Modified libjpeg to return DCT coefficients. Blocks of 8x8. On ResNet50, 1.77x faster, same accuracy.
- [On using CNN with DCT based Image Data](https://www.scss.tcd.ie/Rozenn.Dahyot/pdf/IMVIP2017_MatejUlicny.pdf). IMVIP 2017.

References

* [JPEG DCT, Discrete Cosine Transform (JPEG Pt2)- Computerphile](https://www.youtube.com/watch?v=Q2aEzeMDHMA).
Excellent visual walkthrough of JPEG compression and decompression. CbCrY,DCT,quantization,Huffman encoding. 

