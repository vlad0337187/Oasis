/**
 * Toon Lines shader by Jose I. Romero (cyborg_ar)
 *
 * Based on blender's built-in "prewitt" filter which is free software
 * released under the terms of the GNU General Public License version 2
 * 
 * The original code is (c) Blender Foundation.
 */
uniform sampler2D bgl_RenderedTexture;
uniform vec2 bgl_TextureCoordinateOffset[9];

#define blurclamp 0.0004 
#define bias 0.1
 
#define KERNEL_SIZE  3.0
	
vec4 blur(vec2 coo)	
{
	 
	vec2 dofblur = vec2(clamp( bias, -blurclamp, blurclamp ));


	vec4 col = vec4( 0, 0, 0, 0 );
	for ( float x = -KERNEL_SIZE + 1.0; x < KERNEL_SIZE; x += 1.0 )
	{
	for ( float y = -KERNEL_SIZE + 1.0; y < KERNEL_SIZE; y += 1.0 )
	{
		 col += texture2D(bgl_RenderedTexture, gl_TexCoord[0].xy + vec2( dofblur.x * x, dofblur.y * y ) );
	}
	}
	col /= ((KERNEL_SIZE+KERNEL_SIZE)-1.0)*((KERNEL_SIZE+KERNEL_SIZE)-1.0);
	 
	return col;
	}





void main(void)
{
    vec4 sample[9];
    vec4 border;
    vec4 texcol = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);

    for (int i = 0; i < 9; i++)
    {
        sample[i] = texture2D(bgl_RenderedTexture, 
                              gl_TexCoord[0].st + bgl_TextureCoordinateOffset[i]);
    }

    vec4 horizEdge = sample[2] + sample[5] + sample[8] -
                     (sample[0] + sample[3] + sample[6]);

    vec4 vertEdge = sample[0] + sample[1] + sample[2] -
                    (sample[6] + sample[7] + sample[8]);

    border.rgb = sqrt((horizEdge.rgb * horizEdge.rgb) + 
                            (vertEdge.rgb * vertEdge.rgb));

       if (border.r > 0.4||border.g > 0.4||border.b > 0.4){
        gl_FragColor = blur(gl_TexCoord[0].st);
    }else{
        gl_FragColor.rgb = texcol.rgb;
        gl_FragColor.a = 1.0;
    }
}