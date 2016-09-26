from bge import logic as g

cont = g.getCurrentController()
own = cont.owner
scene = g.getCurrentScene()
camera = scene.active_camera

Amount = own['Amount']
Timer = own['Timer']
Speed = own['Speed']
Scale = own['Scale']
Sharpness = own['Sharpness']

 
VertexShader = """

varying vec3 vertexpos, N, L;
void main()
{


	N = normalize(gl_NormalMatrix * gl_Normal);
	L = normalize(gl_LightSource[0].position.xyz);
	

	vertexpos = gl_Vertex.xyz;
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	
}

 
"""
 
 
 
FragmentShader = """
 
const float permTexUnit = 1.0/128.0;		// Perm texture texel-size
const float permTexUnitHalf = 0.5/128.0;	// Half perm texture texel-size


vec4 rnm(vec2 co){
	float noiseR =  (fract(sin(dot(co ,vec2(12.9898,78.233))) * 43758.5453));
	float noiseG =  (fract(sin(dot(co ,vec2(12.9898,78.233)*2.0)) * 43758.5453)); 
	float noiseB =  (fract(sin(dot(co ,vec2(12.9898,78.233)*3.0)) * 43758.5453));
	float noiseA =  (fract(sin(dot(co ,vec2(12.9898,78.233)*4.0)) * 43758.5453));
	
	return vec4(noiseR,noiseG,noiseB,noiseA);
}



float fade(in float t) {
	return t*t*t*(t*(t*6.0-15.0)+10.0); // this is default value
}

float fnoise3D(in vec3 p)
{
	vec3 pi = permTexUnit*floor(p)+permTexUnitHalf; // Integer part, scaled so +1 moves permTexUnit texel
	// and offset 1/2 texel to sample texel centers
	vec3 pf = fract(p);     // Fractional part for interpolation

	// Noise contributions from (x=0, y=0), z=0 and z=1
	float perm00 = rnm(pi.xy).a ;
	vec3  grad000 = rnm(vec2(perm00, pi.z)).rgb * 4.0 - 1.0;
	float n000 = dot(grad000, pf);
	vec3  grad001 = rnm(vec2(perm00, pi.z + permTexUnit)).rgb * 4.0 - 1.0;
	float n001 = dot(grad001, pf - vec3(0.0, 0.0, 1.0));

	// Noise contributions from (x=0, y=1), z=0 and z=1
	float perm01 = rnm(pi.xy + vec2(0.0, permTexUnit)).a ;
	vec3  grad010 = rnm(vec2(perm01, pi.z)).rgb * 4.0 - 1.0;
	float n010 = dot(grad010, pf - vec3(0.0, 1.0, 0.0));
	vec3  grad011 = rnm(vec2(perm01, pi.z + permTexUnit)).rgb * 4.0 - 1.0;
	float n011 = dot(grad011, pf - vec3(0.0, 1.0, 1.0));

	// Noise contributions from (x=1, y=0), z=0 and z=1
	float perm10 = rnm(pi.xy + vec2(permTexUnit, 0.0)).a ;
	vec3  grad100 = rnm(vec2(perm10, pi.z)).rgb * 4.0 - 1.0;
	float n100 = dot(grad100, pf - vec3(1.0, 0.0, 0.0));
	vec3  grad101 = rnm(vec2(perm10, pi.z + permTexUnit)).rgb * 4.0 - 1.0;
	float n101 = dot(grad101, pf - vec3(1.0, 0.0, 1.0));

	// Noise contributions from (x=1, y=1), z=0 and z=1
	float perm11 = rnm(pi.xy + vec2(permTexUnit, permTexUnit)).a ;
	vec3  grad110 = rnm(vec2(perm11, pi.z)).rgb * 4.0 - 1.0;
	float n110 = dot(grad110, pf - vec3(1.0, 1.0, 0.0));
	vec3  grad111 = rnm(vec2(perm11, pi.z + permTexUnit)).rgb * 4.0 - 1.0;
	float n111 = dot(grad111, pf - vec3(1.0, 1.0, 1.0));

	// Blend contributions along x
	vec4 n_x = mix(vec4(n000, n001, n010, n011),
			vec4(n100, n101, n110, n111), fade(pf.x));

	// Blend contributions along y
	vec2 n_xy = mix(n_x.xy, n_x.zw, fade(pf.y));

	// Blend contributions along z
	float n_xyz = mix(n_xy.x, n_xy.y, fade(pf.z));

	// We're done, return the final noise value.
	return n_xyz;
}


uniform float Speed, Timer, Scale, Sharpness, Amount;	


///////////////
// Main Loop //
///////////////
varying vec3 vertexpos, N, L;


void main()
{

	vec3 DSpeed = vec3(Speed / 4.0, Speed / 4.0, Speed / 4.0);

	float clouds = Amount;
	clouds += fnoise3D((vertexpos*Scale)+(Timer*DSpeed))*0.1;
	clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.05))+(Timer*DSpeed))*2.0)/2.0);
	clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.10))+(Timer*DSpeed))*4.0)/4.0);
	clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.15))+(Timer*DSpeed))*8.0)/8.0);
	clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.16))+(Timer*DSpeed))*16.0)/16.0);
	clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.16))+(Timer*DSpeed))*32.0)/32.0);
	clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.16))+(Timer*DSpeed))*64.0)/64.0);
	//clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.16))+(Timer*DSpeed))*128.0)/128.0);
	//clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.16))+(Timer*DSpeed))*256.0)/256.0); //было раскомментировано
	//clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.16))+(Timer*DSpeed))*512.0)/512.0);
	//clouds += abs(fnoise3D(((vertexpos*Scale+(clouds*0.16))+(Timer*DSpeed))*1024.0)/1024.0);
	
	clouds = pow((clouds),Sharpness);
	
		
	//vec3 normal = normalize(N); //было раскомментировано, но вроде как не нужно
	//vec3 Diffuse = max(dot(normal, L),0.0); //было раскомментировано, но вроде как не нужно
	// Эти штуки нужны для других способов формирования gl_FragColor
	
	//gl_FragColor = vec4(Diffuse.xyz,1.0);
	//gl_FragColor = vec4(Diffuse*vertexpos.z,clouds);
	
	//gl_FragColor = vec4(1.0,1.0,1.0,clouds);
	gl_FragColor = vec4(0.9,0.9,0.9,clouds);
	//gl_FragColor = vec4(0.61,0.64,0.62,1.0) * vec4(Diffuse.xyz,1.0)*0.8+0.2;
	//gl_FragColor.a = clouds;
}

 
"""

mesh = own.meshes[0]
for mat in mesh.materials:
	shader = mat.getShader()
	if shader != None:
		if not shader.isValid():
			shader.setSource(VertexShader, FragmentShader, 1)

		shader.setUniform1f('Timer',Timer)
		shader.setUniform1f('Speed',Speed)
		shader.setUniform1f('Scale',Scale)
		shader.setUniform1f('Sharpness',Sharpness) 
		shader.setUniform1f('Amount',Amount)