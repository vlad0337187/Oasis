uniform sampler2D bgl_DepthTexture;
uniform sampler2D bgl_RenderedTexture;
uniform float bgl_RenderedTextureWidth;
uniform float bgl_RenderedTextureHeight;

#define PI    3.14159265

float width = bgl_RenderedTextureWidth; //texture width
float height = bgl_RenderedTextureHeight; //texture height

float near = 0.1; //Z-near
float far = 80.0; //Z-far

int samples = 1; //samples on the first ring (default = 5)
int rings = 2; //ring count (default = 3)

vec2 texCoord = gl_TexCoord[0].st;

vec2 rand(in vec2 coord) //generating random noise
{
	float noiseX = (fract(sin(dot(coord ,vec2(12.9898,78.233))) * 43758.5453));
	float noiseY = (fract(sin(dot(coord ,vec2(12.9898,78.233)*2.0)) * 43758.5453));
	return vec2(noiseX,noiseY);
}


float readDepth(in vec2 coord) 
{
	if (gl_TexCoord[3].x<0.0||gl_TexCoord[3].y<0.0) return 1.0;
	return (2.0 * near) / (far + near - texture2D(bgl_DepthTexture, coord ).x * (far-near)); 	
}

float compareDepths(in float depth1, in float depth2,inout int far)     
{       
	float diff = (depth1 - depth2)*100.0; //depth difference (0-100)     
	float gdisplace = 0.5; //gauss bell center     
	float garea = 1.0; //gauss bell width 2     
	//reduce left bell width to avoid self-shadowing     
	if (diff<gdisplace)
	{         
	garea = 0.7;     
	}else{
	far = 1;     
	}     
	
	float gauss = pow(2.7182,-2.0*(diff-gdisplace)*(diff-gdisplace)/(garea*garea));
	return gauss;
}  

float calAO(float depth,float dw, float dh)     
{   
    float dd = (1.0-depth)*0.7;
	float temp = 0.0;     
	float temp2 = 0.0;     
	float coordw = gl_TexCoord[0].x + dw*dd;     
	float coordh = gl_TexCoord[0].y + dh*dd;     
	float coordw2 = gl_TexCoord[0].x - dw*dd;     
	float coordh2 = gl_TexCoord[0].y - dh*dd;     
	

	vec2 coord = vec2(coordw , coordh);
    vec2 coord2 = vec2(coordw2, coordh2);
    int far = 0;     	
	temp = compareDepths(depth, readDepth(coord),far);        
	//DEPTH EXTRAPOLATION:        
	if (far > 0)
	{          
		temp2 = compareDepths(readDepth(coord2),depth,far);          
		temp += (1.0-temp)*temp2;
	}      
	
	return temp; 
	
} 

void main(void)
{	
	vec2 noise = rand(texCoord)*0.001; 
	float depth = readDepth(texCoord);
	float d;
	
	float aspect = width/height;
	
	float w = (1.0 / width)/clamp(depth,0.25,1.0)+(noise.x*(1.0-noise.x));
	float h = (1.0 / height)/clamp(depth,0.25,1.0)+(noise.y*(1.0-noise.y));
	
	float pw;
	float ph;

	float ao;	
	float s;
	
	int ringsamples;
	
	for (int i = 1; i <= rings; i += 1)
	{   
		ringsamples = i * samples;   
		for (int j = 0 ; j < ringsamples ; j += 1)   
		{      
			float step = PI*2.0 / float(ringsamples);      
			pw = (cos(float(j)*step)*float(i));      
			ph = (sin(float(j)*step)*float(i));          
			ao += calAO(depth,pw*w,ph*h);      
			s += 1.0;   
		}
	}

	
	ao /= s;
	ao = 1.0-ao;	

    vec3 color = texture2D(bgl_RenderedTexture,texCoord).rgb;
    
    vec3 lumcoeff = vec3(0.299,0.587,0.114);
	float lum = dot(color.rgb, lumcoeff);
	vec3 luminance = vec3(lum, lum, lum);

	//luminance = clamp( max(0.0,luminance-0.2) + max(0.0,luminance-0.2) + max(0.0,luminance-0.2), 0.0, 1.0);

	gl_FragColor = vec4(vec3(color*mix(vec3(ao),vec3(1.0),luminance)),1.0);
    //gl_FragColor = vec4(vec3(ao),1.0);
}