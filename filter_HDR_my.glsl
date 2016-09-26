uniform sampler2D bgl_LuminanceTexture;
uniform sampler2D bgl_RenderedTexture;

uniform float HDRthreshold; // from 0 to 1; default = 0.5; 
uniform float HDRamount; // from 0 to 1

vec2 texcoord = vec2(gl_TexCoord[0]).st;



void main(void)
{
	vec4 value =  texture2D(bgl_RenderedTexture, texcoord);
    float mid_value = (value[0] + value[1] + value[2]) / 3.0;
    vec4 shit = vec4(0.0, 1.0, 0.0, 1.0);	

    float amount = 100.0 - HDRamount * 100;
    
    float a = -4.0;
    float b = abs(a);
    
    if (mid_value > HDRthreshold) {
        gl_FragColor = 
                    vec4(
                    value[0] + ((1.0 - value[0]) / amount),
                    value[1] + ((1.0 - value[1]) / amount),
                    value[2] + ((1.0 - value[2]) / amount),
                    value[3]);
    }
    if (mid_value < HDRthreshold) {
        gl_FragColor =  
                    vec4(
                    value[0] - ((1.0 - value[0]) / amount),
                    value[1] - ((1.0 - value[1]) / amount),
                    value[2] - ((1.0 - value[2]) / amount),
                    value[3]);
    }
    if (mid_value == HDRthreshold) {
        gl_FragColor = value;
    }
}
