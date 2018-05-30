using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using UnityEngine;

public class CameraHandler : MonoBehaviour {

	public Transform Target;
	public GameObject Scene;
	public GameObject MarkedObject;
	public Material WoodenMat;
	public Material MarkedMat;
	public int AmoutScreenshot;

	private bool isCoroutineFinished = true;


	public string ScreenshotDir
	{
		get { return Application.streamingAssetsPath + "/ScreenShots"; }
	}

	private int index;

	private void Start()
	{
		index = 0;
	}

	// Update is called once per frame
	void Update ()
	{

		//if (Input.GetKeyDown("c"))
		//{
		if (index < AmoutScreenshot && isCoroutineFinished)
		{
			isCoroutineFinished = false;
			transform.position = SetRandomCameraPos();
			Debug.Log("Camera Random Pos " + transform.position);
			transform.LookAt(Target);
			StartCoroutine(TakeScreenshots());
		}
		//}
	}

	/// <summary>
	/// 
	/// </summary>
	/// <returns></returns>
	private Vector3 SetRandomCameraPos()
	{
		Vector3 newPosition;

		// creates a position on the positive hemisphere in terms of y
		do
		{
			newPosition = Random.insideUnitSphere * 50;
			//wird ausgeführt, bis der Ausdruck false ergibt 
			Debug.Log("inside" + IsInsideBuilding(newPosition));
		} while (newPosition.y < 3 || IsInsideBuilding(newPosition));


		return newPosition;
	}

	/// <summary>
	/// 
	/// </summary>
	public IEnumerator TakeScreenshots()
	{
		//takes a screenshot from the cameraview 
		SetMaterialOfObject(MarkedObject, WoodenMat);
		yield return StartCoroutine(CaptureScreenshot(false));

		SetMaterialOfObject(MarkedObject, MarkedMat);
		yield return StartCoroutine(CaptureScreenshot(true));

		index++;

		isCoroutineFinished = true;
	}

	/// <summary>
	/// 
	/// </summary>
	/// <param name="pos"></param>
	/// <returns></returns>
	public bool IsInsideBuilding(Vector3 pos)
	{
		foreach (Transform child in Scene.transform)
		{
			if (child.GetComponent<BoxCollider>() != null && child.GetComponent<BoxCollider>().bounds.Contains(pos))
			{
				Debug.Log("INSIDE BUILDING" + pos);
				return true;
			}

			if (child.GetComponent<SphereCollider>() != null && child.GetComponent<SphereCollider>().bounds.Contains(pos))
			{
				Debug.Log("INSIDE BUILDING" + pos);
				return true;
			}
		}
		return false;
	}

	private void SetMaterialOfObject(GameObject go, Material material)
	{
		go.GetComponent<Renderer>().material = material;
		foreach (Transform child in go.transform)
		{
			child.GetComponent<Renderer>().material = material;
		}
	}

	IEnumerator CaptureScreenshot(bool isMarked)
	{
		yield return new WaitForEndOfFrame();

		string ScreenshotName = "screenshot" + index + ".png";

		if (isMarked) ScreenshotName = "screenshot" + index + "_marked" + ".png";

		string path = Path.Combine(ScreenshotDir, ScreenshotName);

		if (!Directory.Exists(ScreenshotDir))
		{
			Directory.CreateDirectory(ScreenshotDir);
		}

		Texture2D screenImage = new Texture2D(Screen.width, Screen.height);
		//Get Image from screen
		screenImage.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
		screenImage.Apply();
		//Convert to png
		byte[] imageBytes = screenImage.EncodeToPNG();

		//Save image to file

		File.WriteAllBytes(path, imageBytes);

		Debug.Log("ANKOMMER: Screenshot to: " + path);
	}



}
